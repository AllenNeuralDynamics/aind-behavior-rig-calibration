from __future__ import annotations

import argparse
import datetime
import glob
import logging
import os
import secrets
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Generic, List, Optional, Tuple, Type, TypeVar, Union

import git
import pydantic
from requests import HTTPError

from aind_behavior_services import (
    AindBehaviorRigModel,
    AindBehaviorSessionModel,
    AindBehaviorTaskLogicModel,
)
from aind_behavior_services.aind_services import data_mapper
from aind_behavior_services.aind_services.watchdog import Watchdog
from aind_behavior_services.base import singleton
from aind_behavior_services.db_utils import SubjectDataBase, SubjectEntry
from aind_behavior_services.utils import run_bonsai_process

TRig = TypeVar("TRig", bound=AindBehaviorRigModel)  # pylint: disable=invalid-name
TSession = TypeVar("TSession", bound=AindBehaviorSessionModel)  # pylint: disable=invalid-name
TTaskLogic = TypeVar("TTaskLogic", bound=AindBehaviorTaskLogicModel)  # pylint: disable=invalid-name


@singleton
class Launcher(Generic[TRig, TSession, TTaskLogic]):
    RIG_DIR = "Rig"
    SUBJECT_DIR = "Subjects"
    TASK_LOGIC_DIR = "TaskLogic"
    VISUALIZERS_DIR = "VisualizerLayouts"

    def __init__(
        self,
        rig_schema_model: Type[TRig],
        session_schema_model: Type[TSession],
        task_logic_schema_model: Type[TTaskLogic],
        data_dir: os.PathLike,
        config_library_dir: os.PathLike,
        bonsai_workflow: os.PathLike,
        temp_dir: os.PathLike = Path("local/.temp"),
        remote_data_dir: Optional[os.PathLike] = None,
        bonsai_executable: os.PathLike = Path("bonsai/bonsai.exe"),
        repository_dir: Optional[os.PathLike] = None,
        bonsai_is_editor_mode: bool = True,
        bonsai_is_start_flag: bool = True,
        allow_dirty: bool = False,
        skip_hardware_validation: bool = False,
        dev_mode: bool = False,
        logger: Optional[logging.Logger] = None,
        watchdog: Optional[Watchdog] = None,
        group_by_subject_log: bool = False,
    ) -> None:
        # Dependency injection
        self.temp_dir = self.abspath(temp_dir) / secrets.token_hex(nbytes=16)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

        self.logger = logger if logger is not None else self._create_logger(self.temp_dir / "launcher.log")

        self.watchdog = watchdog

        args = self._cli_wrapper()

        repository_dir = Path(args.repository_dir) if args.repository_dir is not None else repository_dir
        if repository_dir is None:
            self.repository = git.Repo()
        else:
            self.repository = git.Repo(path=repository_dir)

        # Always work from the root of the repository
        self._cwd = self.repository.working_dir
        os.chdir(self._cwd)

        # Schemas
        self.rig_schema_model = rig_schema_model
        self.session_schema_model = session_schema_model
        self.task_logic_schema_model = task_logic_schema_model

        self._rig_schema: Optional[TRig] = None
        self._session_schema: Optional[TSession] = None
        self._task_logic_schema: Optional[TTaskLogic] = None
        self._bonsai_visualizer_layout: Optional[str] = None

        # Directories
        self.data_dir = Path(args.data_dir) if args.data_dir is not None else self.abspath(data_dir)
        self.remote_data_dir = (
            Path(args.remote_data_dir)
            if args.remote_data_dir is not None
            else (self.abspath(remote_data_dir) if remote_data_dir is not None else None)
        )
        self.bonsai_executable = self.abspath(bonsai_executable)
        self.default_bonsai_workflow = (
            Path(args.bonsai_workflow) if args.bonsai_workflow is not None else self.abspath(bonsai_workflow)
        )
        # Derived directories
        self.config_library_dir = (
            Path(args.config_library_dir)
            if args.config_library_dir is not None
            else self.abspath(Path(config_library_dir))
        )
        self.computer_name = os.environ["COMPUTERNAME"]
        self._dev_mode = args.dev_mode if args.dev_mode else dev_mode
        if self._dev_mode:
            self.logger.setLevel(logging.DEBUG)

        self._rig_dir = Path(os.path.join(self.config_library_dir, self.RIG_DIR, self.computer_name))
        self._subject_dir = Path(os.path.join(self.config_library_dir, self.SUBJECT_DIR))
        self._task_logic_dir = Path(os.path.join(self.config_library_dir, self.TASK_LOGIC_DIR))
        self._visualizer_layouts_dir = Path(
            os.path.join(self.config_library_dir, self.VISUALIZERS_DIR, self.computer_name)
        )
        # Flags
        self.bonsai_is_editor_mode = args.bonsai_is_editor_mode if args.bonsai_is_editor_mode else bonsai_is_editor_mode
        self.bonsai_is_start_flag = args.bonsai_is_start_flag if args.bonsai_is_start_flag else bonsai_is_start_flag
        self.allow_dirty = args.allow_dirty if args.allow_dirty else allow_dirty
        self.skip_hardware_validation = (
            args.skip_hardware_validation if args.skip_hardware_validation else skip_hardware_validation
        )
        self.group_by_subject_log = group_by_subject_log

        self._subject_db_data: Optional[SubjectEntry] = None
        self._run_hook_return: Any = None

        self.post_init_hook(args)

    @property
    def rig_schema(self) -> TRig:
        if self._rig_schema is None:
            raise ValueError("Rig schema instance not set.")
        return self._rig_schema

    @property
    def session_schema(self) -> TSession:
        if self._session_schema is None:
            raise ValueError("Session schema instance not set.")
        return self._session_schema

    @property
    def task_logic_schema(self) -> TTaskLogic:
        if self._task_logic_schema is None:
            raise ValueError("Task logic schema instance not set.")
        return self._task_logic_schema

    def run(self):  # For backwards compatibility
        self.run_ui()

    def post_init_hook(self, cli_args: argparse.Namespace) -> None:
        """Overridable method that runs at the end of the self.__init__ method"""
        if cli_args.create_directories is True:
            self._make_folder_structure()

    @staticmethod
    def _exit(code: int = 0) -> None:
        sys.exit(code)

    def _print_diagnosis(self) -> None:
        """
        Prints the diagnosis information for the launcher.

        This method prints the diagnosis information,
        including the computer name, data directory,
        and config library directory.

        Parameters:
            None

        Returns:
            None
        """
        self.logger.debug(
            "-------------------------------\n"
            "Diagnosis:\n"
            "-------------------------------\n"
            "Current Directory: %s\n"
            "Repository: %s\n"
            "Computer Name: %s\n"
            "Data Directory: %s\n"
            "Remote Data Directory: %s\n"
            "Config Library Directory: %s\n"
            "Temporary Directory: %s\n"
            "Log Directory: %s\n"
            "Bonsai Executable: %s\n"
            "Default Workflow: %s\n"
            "-------------------------------",
            self._cwd,
            self.repository.working_dir,
            self.computer_name,
            self.data_dir,
            self.remote_data_dir,
            self.config_library_dir,
            self.temp_dir,
            self.bonsai_executable,
            self.default_bonsai_workflow,
        )

    def _print_header(self) -> None:
        """
        Prints the header information for the launcher.

        This method prints the header information, including the task logic schema version,
        rig schema version, and session schema version.

        Parameters:
            None

        Returns:
            None
        """

        _HEADER = r"""

        ██████╗██╗      █████╗ ██████╗ ███████╗
        ██╔════╝██║     ██╔══██╗██╔══██╗██╔════╝
        ██║     ██║     ███████║██████╔╝█████╗
        ██║     ██║     ██╔══██║██╔══██╗██╔══╝
        ╚██████╗███████╗██║  ██║██████╔╝███████╗
        ╚═════╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝

        Command-line-interface Launcher for AIND Behavior Experiments
        Press Control+C to exit at any time.
        """

        _str = (
            "-------------------------------\n"
            f"{_HEADER}\n"
            f"TaskLogic ({self.task_logic_schema_model.__name__}) Schema Version: {self.task_logic_schema_model.model_construct().version}\n"
            f"Rig ({self.rig_schema_model.__name__}) Schema Version: {self.rig_schema_model.model_construct().version}\n"
            f"Session ({self.session_schema_model.__name__}) Schema Version: {self.session_schema_model.model_construct().version}\n"
            "-------------------------------"
        )

        self.logger.info(_str)
        if self._dev_mode:
            self._print_diagnosis()

    def _save_temp_model(self, model: Union[TRig, TSession, TTaskLogic], folder: Optional[os.PathLike]) -> str:
        """
        Saves the given model as a JSON file in the specified folder or in the default temporary folder.

        Args:
            model (BaseModel): The model to be saved.
            folder (Optional[os.PathLike]):
              The folder where the model should be saved.
              If not provided, the default temporary folder will be used.

        Returns:
            str: The file path of the saved model.

        """
        folder = Path(folder) if folder is not None else Path(self.temp_dir)
        os.makedirs(folder, exist_ok=True)
        fname = model.__class__.__name__ + ".json"
        fpath = os.path.join(folder, fname)
        with open(fpath, "w+", encoding="utf-8") as f:
            f.write(model.model_dump_json(indent=3))
        return fpath

    TModel = TypeVar("TModel", bound=pydantic.BaseModel)  # pylint: disable=invalid-name

    @staticmethod
    def _load_model_from_json(json_path: os.PathLike | str, model: type[TModel]) -> TModel:
        with open(Path(json_path), "r", encoding="utf-8") as file:
            return model.model_validate_json(file.read())

    def _validate_dependencies(self) -> None:
        """
        Validates the dependencies required for the launcher to run.
        """
        try:
            if not (os.path.isfile(self.bonsai_executable)):
                raise FileNotFoundError(f"Bonsai executable (bonsai.exe) not found! Expected {self.bonsai_executable}.")
            if not (os.path.isdir(self.config_library_dir)):
                raise FileNotFoundError(f"Config library not found! Expected {self.config_library_dir}.")
            if not (os.path.isdir(os.path.join(self.config_library_dir, "Rig", self.computer_name))):
                raise FileNotFoundError(
                    f"Rig configuration not found! \
                        Expected {os.path.join(self.config_library_dir, self.RIG_DIR, self.computer_name)}."
                )
            if not (os.path.isfile(os.path.join(self.default_bonsai_workflow))):
                raise FileNotFoundError(f"Bonsai workflow file not found! Expected {self.default_bonsai_workflow}.")

            if self.watchdog is not None:
                self.logger.warning("Watchdog service is enabled.")
                if not self.watchdog.is_running():
                    self.logger.warning(
                        "Watchdog service is not running. \
                                        After the session is over, \
                                        the launcher will attempt to forcefully restart it"
                    )
                if not self.watchdog.validate_project_name():
                    try:
                        self.logger.warning("Watchdog project name is not valid.")
                    except HTTPError as e:
                        self.logger.error("Failed to fetch project names from endpoint. %s", e)
            else:
                self.logger.warning("Watchdog service is disabled.")

            if self.repository.is_dirty():
                self.logger.warning(
                    "Git repository is dirty. Discard changes before continuing unless you know what you are doing!"
                )
                if not self.allow_dirty:
                    self.logger.error(
                        "Dirty repository not allowed. Exiting. Consider running with --allow-dirty flag."
                    )
                    self._exit(-1)
        except Exception as e:
            self.logger.error("Failed to validate dependencies. %s", e)
            self._exit(-1)
            raise e

    @staticmethod
    def _prompt_pick_file_from_list(
        available_files: list[str],
        prompt: str = "Choose a file:",
        override_zero: Tuple[Optional[str], Optional[str]] = ("Enter manually", None),
    ) -> str:
        print(prompt)
        if override_zero[0] is not None:
            print(f"0: {override_zero[0]}")
        _ = [print(f"{i+1}: {os.path.split(file)[1]}") for i, file in enumerate(available_files)]
        choice = int(input("Choice: "))
        if choice < 0 or choice >= len(available_files) + 1:
            raise ValueError
        if choice == 0:
            if override_zero[0] is None:
                raise ValueError
            if override_zero[1] is not None:
                return override_zero[1]
            else:
                path = str(input(override_zero[0]))
            return path
        else:
            return available_files[choice - 1]

    @staticmethod
    def _prompt_yes_no_question(prompt: str) -> bool:
        while True:
            reply = input(prompt + " (Y\\N): ").upper()
            if reply == "Y" or reply == "1":
                return True
            elif reply == "N" or reply == "0":
                return False
            else:
                print("Invalid input. Please enter 'Y' or 'N'.")

    def _prompt_session_input(self, folder: Optional[str] = None) -> TSession:
        _local_config_folder = (
            Path(os.path.join(self.config_library_dir, folder)) if folder is not None else self._subject_dir
        )
        available_batches = self._get_available_batches(_local_config_folder)

        subject_list = self._get_subject_list(available_batches)
        subject = self._choose_subject(subject_list)
        self._subject_db_data = subject_list.get_subject(subject)
        notes = self.prompt_get_notes()

        return self.session_schema_model(
            experiment="",  # Will be set later
            root_path=str(self.data_dir.resolve())
            if not self.group_by_subject_log
            else str(self.data_dir.resolve() / subject),
            remote_path=str(self.remote_data_dir.resolve()) if self.remote_data_dir is not None else None,
            subject=subject,
            notes=notes,
            commit_hash=self.repository.head.commit.hexsha,
            allow_dirty_repo=self._dev_mode or self.allow_dirty,
            skip_hardware_validation=self.skip_hardware_validation,
            experiment_version="",  # Will be set later
        )

    def _get_available_batches(self, folder: os.PathLike) -> List[str]:
        available_batches = glob.glob(os.path.join(folder, "*.json"))
        available_batches = [batch for batch in available_batches if os.path.isfile(batch)]
        if len(available_batches) == 0:
            raise FileNotFoundError(f"No batch files found in {folder}")
        return available_batches

    def _get_subject_list(self, available_batches: List[str]) -> SubjectDataBase:
        subject_list = None
        while subject_list is None:
            try:
                if len(available_batches) == 1:
                    batch_file = available_batches[0]
                    print(f"Found a single session config file. Using {batch_file}.")
                else:
                    batch_file = self._prompt_pick_file_from_list(
                        available_batches, prompt="Choose a batch:", override_zero=(None, None)
                    )
                    if not os.path.isfile(batch_file):
                        raise FileNotFoundError(f"File not found: {batch_file}")
                    print(f"Using {batch_file}.")
                with open(batch_file, "r", encoding="utf-8") as file:
                    subject_list = SubjectDataBase.model_validate_json(file.read())
                if len(subject_list.subjects) == 0:
                    raise ValueError("No subjects found in the batch file.")
            except (ValueError, FileNotFoundError, IOError, pydantic.ValidationError) as e:
                self.logger.error("Invalid choice. Try again. %s", e)
                if len(available_batches) == 1:
                    self.logger.error("No valid subject batch files found. Exiting.")
                    self._exit(-1)
            else:
                return subject_list

    def _choose_subject(self, subject_list: SubjectDataBase) -> str:
        subject = None
        while subject is None:
            try:
                subject = self._prompt_pick_file_from_list(
                    list(subject_list.subjects.keys()), prompt="Choose a subject:", override_zero=(None, None)
                )
            except ValueError as e:
                self.logger.error("Invalid choice. Try again. %s", e)
        return subject

    @staticmethod
    def prompt_get_notes() -> str:
        notes = str(input("Enter notes:"))
        return notes

    def _prompt_rig_input(self, folder_name: Optional[str] = None) -> TRig:
        rig_schemas_path = (
            Path(os.path.join(self.config_library_dir, folder_name, self.computer_name))
            if folder_name is not None
            else self._rig_dir
        )
        available_rigs = glob.glob(os.path.join(rig_schemas_path, "*.json"))
        if len(available_rigs) == 1:
            print(f"Found a single rig config file. Using {available_rigs[0]}.")
            return self._load_model_from_json(available_rigs[0], self.rig_schema_model)
        else:
            while True:
                try:
                    path = self._prompt_pick_file_from_list(
                        available_rigs, prompt="Choose a rig:", override_zero=(None, None)
                    )
                    rig = self._load_model_from_json(path, self.rig_schema_model)
                    print(f"Using {path}.")
                    return rig
                except pydantic.ValidationError as e:
                    self.logger.error("Failed to validate pydantic model. Try again. %s", e)
                except ValueError as e:
                    self.logger.error("Invalid choice. Try again. %s", e)

    def _prompt_task_logic_input(
        self, folder: Optional[str] = None, hint_input: Optional[SubjectEntry] = None
    ) -> TTaskLogic:
        _path = Path(os.path.join(self.config_library_dir, folder)) if folder is not None else self._task_logic_dir

        task_logic: Optional[TTaskLogic] = None
        while task_logic is None:
            try:
                if hint_input is None:
                    available_files = glob.glob(os.path.join(_path, "*.json"))
                    path = self._prompt_pick_file_from_list(
                        available_files, prompt="Choose a task logic:", override_zero=(None, None)
                    )
                    if not os.path.isfile(path):
                        raise FileNotFoundError(f"File not found: {path}")
                    task_logic = self._load_model_from_json(path, self.task_logic_schema_model)
                    print(f"Using {path}.")

                else:
                    hinted_path = os.path.join(_path, hint_input.task_logic_target + ".json")
                    if not os.path.isfile(hinted_path):
                        hint_input = None
                        raise FileNotFoundError(f"Hinted file not found: {hinted_path}. Try entering manually.")
                    use_hint = self._prompt_yes_no_question(f"Would you like to go with the task file: {hinted_path}?")
                    if use_hint:
                        task_logic = self._load_model_from_json(hinted_path, self.task_logic_schema_model)
                    else:
                        hint_input = None

            except pydantic.ValidationError as e:
                self.logger.error("Failed to validate pydantic model. Try again. %s", e)
            except (ValueError, FileNotFoundError) as e:
                self.logger.error("Invalid choice. Try again. %s", e)

        return task_logic

    def _prompt_visualizer_layout_input(self, folder_name: Optional[str] = None) -> Optional[str]:
        layout_schemas_path = (
            Path(os.path.join(self.config_library_dir, folder_name, self.computer_name))
            if folder_name is not None
            else self._visualizer_layouts_dir
        )
        available_layouts = glob.glob(os.path.join(layout_schemas_path, "*.bonsai.layout"))
        while True:
            try:
                print("Pick a visualizer layout:")
                print("0: Default")
                print("1: None")
                _ = [print(f"{i+2}: {os.path.split(file)[1]}") for i, file in enumerate(available_layouts)]
                choice = int(input("Choice: "))
                if choice < 0 or choice >= len(available_layouts) + 2:
                    raise ValueError
                if choice == 0:
                    return None
                if choice == 1:
                    return ""
                else:
                    return available_layouts[choice - 2]
            except ValueError as e:
                self.logger.error("Invalid choice. Try again. %s", e)

    def pre_run_hook(self, *args, **kwargs):
        self.logger.info("Pre-run hook started.")

    def post_run_hook(self, *args, **kwargs):
        self.logger.info("Post-run hook started.")
        if self._run_hook_return is not None:
            self.logger.info("Run hook returned %s", self._run_hook_return)
        try:
            self.logger.info("Mapping to aind-data-schema Session: %s.")
            aind_data_schema_session = self._map_to_aind_data_schema_session()
            aind_data_schema_session.write_standard_file(self.session_schema.root_path)
            self.logger.info("Mapping successful.")
        except (pydantic.ValidationError, ValueError, IOError) as e:
            self.logger.error("Failed to map to aind-data-schema Session. %s", e)
        else:
            if self.watchdog is not None:
                if not self.watchdog.is_running():
                    self.logger.warning("Watchdog service is not running. Attempting to start it.")

                    try:
                        self.watchdog.force_restart(kill_if_running=False)
                    except subprocess.CalledProcessError as e:
                        self.logger.error("Failed to start watchdog service. %s", e)
                    else:
                        if not self.watchdog.is_running():
                            self.logger.error("Failed to start watchdog service.")
                        else:
                            self.logger.info("Watchdog service restarted successfully.")

                self.logger.info("Creating watchdog manifest config.")
                watchdog_manifest_config = self.watchdog.create_manifest_config_from_session(
                    session=self.session_schema, aind_data_schema_session=aind_data_schema_session
                )
                _manifest_path = self.watchdog.dump_manifest_config(watchdog_manifest_config)
                self.logger.info("Watchdog manifest config created successfully at %s.", _manifest_path)

    def run_hook(self, *args, **kwargs) -> None:
        self.logger.info("Running hook started.")
        if self._session_schema is None:
            raise ValueError("Session schema instance not set.")
        if self._task_logic_schema is None:
            raise ValueError("Task logic schema instance not set.")
        if self._rig_schema is None:
            raise ValueError("Rig schema instance not set.")

        additional_properties = {
            "TaskLogicPath": os.path.abspath(
                self._save_temp_model(model=self._task_logic_schema, folder=self.temp_dir)
            ),
            "SessionPath": os.path.abspath(self._save_temp_model(model=self._session_schema, folder=self.temp_dir)),
            "RigPath": os.path.abspath(self._save_temp_model(model=self._rig_schema, folder=self.temp_dir)),
        }

        # _date = self._session_schema.date.strftime("%Y%m%dT%H%M%S")
        self.logger.info("Bonsai process running...")
        proc = run_bonsai_process(
            bonsai_exe=self.bonsai_executable,
            workflow_file=self.default_bonsai_workflow,
            additional_properties=additional_properties,
            layout=self._bonsai_visualizer_layout,
            is_editor_mode=self.bonsai_is_editor_mode,
            is_start_flag=self.bonsai_is_start_flag,
            cwd=self._cwd,
            print_cmd=self._dev_mode,
        )
        if self.bonsai_is_editor_mode:
            self.logger.warning("Bonsai is running in editor mode. Cannot assert successful completion.")
        try:
            proc.check_returncode()
        except subprocess.CalledProcessError as e:
            self.logger.error("Bonsai process exited with an error. \n%s", e)
            self._log_process_std_output("Bonsai", proc)
            self._exit(-1)
        else:
            self._log_process_std_output("Bonsai", proc)
            self.logger.info("Bonsai process completed.")

            if len(proc.stderr) > 0:
                self.logger.error("Bonsai process finished with errors.")
                _continue = self._prompt_yes_no_question("Would you still like to continue?")
                if not _continue:
                    self.logger.info("User chose to exit.")
                    self._exit(-1)
            self._run_hook_return = None  # TODO To be improved

    def _log_process_std_output(self, process_name: str, proc: subprocess.CompletedProcess) -> None:
        if len(proc.stdout) > 0:
            self.logger.info("%s full stdout dump: \n%s", process_name, proc.stdout)
        if len(proc.stderr) > 0:
            self.logger.error("%s full stderr dump: \n%s", process_name, proc.stderr)

    def run_ui(self) -> None:
        try:
            self._print_header()
            self._validate_dependencies()
            self._session_schema = self._prompt_session_input()
            self._task_logic_schema = self._prompt_task_logic_input(hint_input=self._subject_db_data)
            self._rig_schema = self._prompt_rig_input()
            self._bonsai_visualizer_layout = self._prompt_visualizer_layout_input()

            # Handle some cross-schema references
            self._session_schema.experiment = self._task_logic_schema.name
            self._session_schema.experiment_version = self._task_logic_schema.version

            input("Press enter to start or Control+C to exit...")
            self.pre_run_hook()
            self.run_hook()
            self.post_run_hook()

            for handler in self.logger.handlers:
                if isinstance(handler, logging.FileHandler):
                    self.logger.info("File handler found in logger. Closing and copying to session directory.")
                    handler.close()

            if self.session_schema.session_name is not None:
                self._copy_tmp_folder(Path(self.session_schema_model.root_path) / self.session_schema.session_name)

            self.logger.info("All hooks finished. Launcher closing.")
            self._exit(0)

        except KeyboardInterrupt:
            self.logger.error("User interrupted the process.")
            self._exit(-1)
            return

    @classmethod
    def abspath(cls, path: os.PathLike) -> Path:
        """
        Returns the absolute path of the given file or directory.

        Args:
            path os.PathLike: The path to the file or directory.

        Returns:
            Path: The absolute path of the file or directory.

        """
        return Path(path).resolve()

    def _make_folder_structure(self) -> None:
        try:
            self._make_folder(self.data_dir)
            self._make_folder(self.config_library_dir)
            self._make_folder(self.temp_dir)
            self._make_folder(self._task_logic_dir)
            self._make_folder(self._rig_dir)
            self._make_folder(self._subject_dir)
            self._make_folder(self._visualizer_layouts_dir)
        except OSError as e:
            self.logger.error("Failed to create folder structure: %s", e)
            self._exit(-1)

    def _make_folder(self, folder: os.PathLike) -> None:
        if not os.path.exists(self.abspath(folder)):
            self.logger.info("Creating  %s", folder)
            try:
                os.makedirs(folder)
            except OSError as e:
                self.logger.error("Failed to create folder %s: %s", folder, e)
                raise e

    @staticmethod
    def _get_default_arg_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()

        parser.add_argument("--data-dir", help="Specify the data directory")
        parser.add_argument("--remote-data-dir", help="Specify the remote data directory")
        parser.add_argument("--repository-dir", help="Specify the repository directory")
        parser.add_argument("--config-library-dir", help="Specify the configuration library directory")
        parser.add_argument("--bonsai-workflow", help="Specify the workflow")
        parser.add_argument(
            "--create-directories",
            help="Specify whether to force create directories",
            action="store_true",
            default=False,
        )
        parser.add_argument("--dev-mode", help="Specify whether to run in dev mode", action="store_true", default=False)
        parser.add_argument(
            "--bonsai-is-editor-mode",
            help="Specify whether to run in Bonsai editor mode",
            action="store_false",
            default=True,
        )
        parser.add_argument(
            "--bonsai-is-start-flag",
            help="Specify whether to start the Bonsai workflow",
            action="store_false",
            default=True,
        )
        parser.add_argument(
            "--allow-dirty", help="Specify whether to allow a dirty repository", action="store_true", default=False
        )
        parser.add_argument(
            "--skip-hardware-validation",
            help="Specify whether to skip hardware validation",
            action="store_true",
            default=False,
        )

        return parser

    @classmethod
    def _cli_wrapper(cls) -> argparse.Namespace:
        parser = cls._get_default_arg_parser()
        args, _ = parser.parse_known_args()
        return args

    @staticmethod
    def _create_logger(output_path: Optional[os.PathLike]) -> logging.Logger:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        if output_path is not None:
            file_handler = logging.FileHandler(Path(output_path))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        return logger

    def _map_to_aind_data_schema_session(self):
        return data_mapper.mapper_from_session_root(
            session_data_root=Path(self.session_schema.root_path).resolve(),
            session_model=self.session_schema_model,
            rig_model=self.rig_schema_model,
            task_logic_model=self.task_logic_schema_model,
            repository=self.repository,
            script_path=Path(self.default_bonsai_workflow).resolve(),
            session_end_time=datetime.datetime.now(),
        )

    def _copy_tmp_folder(self, dst: os.PathLike) -> None:
        dst = Path(dst) / ".tmp"
        shutil.copytree(self.temp_dir, dst, dirs_exist_ok=True)
