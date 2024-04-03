import glob
import os
import secrets
from typing import Generic, List, Optional, Tuple, Type, TypeVar, Union, Dict

import git
from aind_behavior_services import AindBehaviorRigModel, AindBehaviorSessionModel, AindBehaviorTaskLogicModel
from aind_behavior_services.utils import open_bonsai_process
from pydantic import ValidationError


TRig = TypeVar("TRig", bound=AindBehaviorRigModel)
TSession = TypeVar("TSession", bound=AindBehaviorSessionModel)
TTaskLogic = TypeVar("TTaskLogic", bound=AindBehaviorTaskLogicModel)


class Launcher(Generic[TRig, TSession, TTaskLogic]):
    """
    The Launcher class is responsible for launching the behavior services.

    It initializes the Launcher object with the provided rig schema, session schema, and task logic schema.

    Attributes:
        rig_schema (Type[AindBehaviorRigModel]): The rig schema for the behavior services.
        session_schema (Type[AindBehaviorSessionModel]): The session schema for the behavior services.
        task_logic_schema (Type[AindBehaviorTaskLogicModel]): The task logic schema for the behavior services.
        config_library_dir (os.PathLike | str): The directory where the config library is located.
        temp_dir (os.PathLike | str): The directory for temporary files.
        log_dir (os.PathLike | str): The directory for log files.
        data_dir (os.PathLike | str): The directory for data files.
        remote_data_dir (Optional[os.PathLike | str]): The directory to log remote data.
        bonsai_executable (os.PathLike | str): The path to the Bonsai executable.
        workflow (os.PathLike | str): The path to the bonsai workflow file.
    """

    RIG_DIR = "Rig"
    SESSION_DIR = "Session"
    TASK_LOGIC_DIR = "TaskLogic"
    VISUALIZERS_DIR = "VisualizerLayouts"

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

    def __init__(
        self,
        rig_schema: Type[TRig],
        session_schema: Type[TSession],
        task_logic_schema: Type[TTaskLogic],
        data_dir: os.PathLike | str = r"C:\data",
        config_library_dir: os.PathLike | str = r"\\allen\aind\scratch\AindBehavior.db\{task}",
        temp_dir: os.PathLike | str = "local/.temp",
        log_dir: os.PathLike | str = "local/.dump",
        remote_data_dir: Optional[os.PathLike | str] = None,
        bonsai_executable: os.PathLike | str = "bonsai/bonsai.exe",
        workflow: os.PathLike | str = "src/main.bonsai",
        repository_dir: Optional[os.PathLike | str] = None,
    ) -> None:
        """
        Initializes a new instance of the Launcher class.

        Parameters:
            rig_schema (Type[AindBehaviorRigModel]): The rig schema for the behavior services.
            session_schema (Type[AindBehaviorSessionModel]): The session schema for the behavior services.
            task_logic_schema (Type[AindBehaviorTaskLogicModel]): The task logic schema for the behavior services.
        """
        try:
            if repository_dir is None:
                self.repository = git.Repo()
            else:
                self.repository = git.Repo(path=repository_dir)
        except git.InvalidGitRepositoryError as e:
            raise e("Not a git repository. Please run from the root of the repository.") from e
        # Always work from the root of the repository
        self._cwd = self.repository.working_dir
        os.chdir(self._cwd)

        self.rig_schema = rig_schema
        self.session_schema = session_schema
        self.task_logic_schema = task_logic_schema
        self.temp_dir = self.abspath(temp_dir)
        self.log_dir = self.abspath(log_dir)
        self.data_dir = self.abspath(data_dir)
        self.remote_data_dir = self.abspath(remote_data_dir) if remote_data_dir is not None else None
        self.bonsai_executable = self.abspath(bonsai_executable)
        self.default_workflow = self.abspath(workflow)
        if not isinstance(config_library_dir, str):
            config_library_dir = str(config_library_dir)
        self.config_library_dir = self.abspath(config_library_dir.format(task=task_logic_schema.__name__))
        self.computer_name = os.environ["COMPUTERNAME"]

        self._dev_mode = False
        self._rig_dir = os.path.join(self.config_library_dir, self.RIG_DIR, self.computer_name)
        self._session_dir = os.path.join(self.config_library_dir, self.SESSION_DIR)
        self._task_logic_dir = os.path.join(self.config_library_dir, self.TASK_LOGIC_DIR)
        self._visualizer_layouts_dir = os.path.join(self.config_library_dir, self.VISUALIZERS_DIR, self.computer_name)

    def _print_diagnosis(self) -> None:
        """
        Prints the diagnosis information for the launcher.

        This method prints the diagnosis information, including the computer name, data directory, and config library directory.

        Parameters:
            None

        Returns:
            None
        """
        print("-------------------------------")
        print("Diagnosis:")
        print("-------------------------------")
        print(f"Current Directory: {self._cwd}")
        print(f"Repository: {self.repository.working_dir}")
        print(f"Computer Name: {self.computer_name}")
        print(f"Data Directory: {self.data_dir}")
        print(f"Remote Data Directory: {self.remote_data_dir}")
        print(f"Config Library Directory: {self.config_library_dir}")
        print(f"Temporary Directory: {self.temp_dir}")
        print(f"Log Directory: {self.log_dir}")
        print(f"Bonsai Executable: {self.bonsai_executable}")
        print(f"Default Workflow: {self.default_workflow}")
        print("-------------------------------")

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
        print("-------------------------------")
        print(self._HEADER)
        print(
            f"TaskLogic ({self.task_logic_schema.__name__}) Schema Version: {self.task_logic_schema.model_construct().schema_version}"
        )
        print(f"Rig ({self.rig_schema.__name__}) Schema Version: {self.rig_schema.model_construct().schema_version}")
        print(
            f"Session ({self.session_schema.__name__}) Schema Version: {self.session_schema.model_construct().schema_version}"
        )
        print("-------------------------------")
        self._dev_mode = input("Press Enter to continue...") == "42"
        if self._dev_mode:
            self._print_diagnosis()

    def save_temp_model(self, model: Union[TRig, TSession, TTaskLogic], folder: Optional[os.PathLike | str]) -> str:
        """
        Saves the given model as a JSON file in the specified folder or in the default temporary folder.

        Args:
            model (BaseModel): The model to be saved.
            folder (Optional[os.PathLike | str]): The folder where the model should be saved. If not provided, the default
                temporary folder will be used.

        Returns:
            str: The file path of the saved model.

        """
        if folder is None:
            folder = self.temp_dir
        os.makedirs(folder, exist_ok=True)
        fname = model.__class__.__name__ + "_" + secrets.token_hex(nbytes=16) + ".json"
        fpath = os.path.join(folder, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(model.model_dump_json(indent=3))
        return fpath

    @staticmethod
    def load_json_model(
        json_path: os.PathLike | str, model: Union[Type[TRig], Type[TSession], Type[TTaskLogic]]
    ) -> Union[TRig, TSession, TTaskLogic]:
        with open(json_path, "r", encoding="utf-8") as file:
            return model.model_validate_json(file.read())

    def _validate_dependencies(self) -> None:
        """
        Validates the dependencies required for the launcher to run.
        """

        if self.repository.is_dirty():
            print(
                "WARNING: Git repository is dirty. Discard changes before continuing unless you know what you are doing!"
            )
            print("Press enter to continue...")
            input()

        if not (os.path.isfile(self.bonsai_executable)):
            raise FileNotFoundError(f"Bonsai executable (bonsai.exe) not found! Expected {self.bonsai_executable}.")
        if not (os.path.isdir(self.config_library_dir)):
            raise FileNotFoundError(f"Config library not found! Expected {self.config_library_dir}.")
        if not (os.path.isdir(os.path.join(self.config_library_dir, "Rig", self.computer_name))):
            raise FileNotFoundError(
                f"Rig configuration not found! Expected {os.path.join(self.config_library_dir, self.RIG_DIR, self.computer_name)}."
            )
        if not (os.path.isfile(os.path.join(self.default_workflow))):
            raise FileNotFoundError(f"Bonsai workflow file not found! Expected {self.default_workflow}.")

    @staticmethod
    def pick_file_from_list(
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
    def prompt_yes_no_question(prompt: str) -> bool:
        while True:
            reply = input(prompt + " (Y\\N): ").upper()
            if reply == "Y":
                return True
            elif reply == "N":
                return False
            else:
                print("Invalid input. Please enter 'Y' or 'N'.")

    def prompt_session_input(self, folder: Optional[str] = None) -> TSession:
        _local_config_folder = (
            os.path.join(self.config_library_dir, folder) if folder is not None else self._session_dir
        )
        available_batches = self._get_available_batches(_local_config_folder)

        subject_list = self._get_subject_list(available_batches)
        subject = self._choose_subject(subject_list)
        notes = self._get_notes()

        return self.session_schema(
            experiment=self.session_schema.__name__,
            root_path=self.data_dir,
            remote_path=self.remote_data_dir,
            subject=subject,
            notes=notes,
            commit_hash=self.repository.head.commit.hexsha,
            allow_dirty_repo=self._dev_mode,
            experiment_version=self.task_logic_schema.model_construct().schema_version,
        )

    def _get_available_batches(self, folder: str) -> List[str]:
        available_batches = glob.glob(os.path.join(folder, "*.*"))
        available_batches = [batch for batch in available_batches if os.path.isfile(batch)]
        if len(available_batches) == 0:
            raise FileNotFoundError(f"No batch files found in {folder}")
        return available_batches

    def _get_subject_list(self, available_batches: List[str]) -> List[str]:
        subject_list = None
        while subject_list is None:
            try:
                if len(available_batches) == 1:
                    batch_file = available_batches[0]
                    print(f"Found a single session config file. Using {batch_file}.")
                else:
                    batch_file = self.pick_file_from_list(
                        available_batches, prompt="Choose a batch:", override_zero=(None, None)
                    )
                    if not os.path.isfile(batch_file):
                        raise FileNotFoundError(f"File not found: {batch_file}")
                    print(f"Using {batch_file}.")
                with open(batch_file, "r", encoding="utf-8") as file:
                    subject_list = file.readlines()
                subject_list = [subject.strip() for subject in subject_list if subject.strip()]
                if len(subject_list) == 0:
                    print(f"No subjects found in {batch_file}")
                    raise ValueError()
            except ValueError:
                print("Invalid choice. Try again.")
            except FileNotFoundError:
                print("Invalid choice. Try again.")
            except IOError:
                print("Invalid choice. Try again.")
        return subject_list

    def _choose_subject(self, subject_list: List[str]) -> str:
        subject = None
        while subject is None:
            try:
                subject = self.pick_file_from_list(subject_list, prompt="Choose a subject:", override_zero=(None, None))
            except ValueError:
                print("Invalid choice. Try again.")
        return subject

    def _get_notes(self) -> str:
        notes = str(input("Enter notes:"))
        return notes

    def prompt_rig_input(self, folder_name: Optional[str] = None) -> TRig:
        rig_schemas_path = (
            os.path.join(self.config_library_dir, folder_name, self.computer_name)
            if folder_name is not None
            else self._rig_dir
        )
        available_rigs = glob.glob(os.path.join(rig_schemas_path, "*.json"))
        if len(available_rigs) == 1:
            print(f"Found a single rig config file. Using {available_rigs[0]}.")
            return self.load_json_model(available_rigs[0], self.rig_schema)
        else:
            while True:
                try:
                    path = self.pick_file_from_list(available_rigs, prompt="Choose a rig:", override_zero=(None, None))
                    rig = self.load_json_model(path, self.rig_schema)
                    print(f"Using {path}.")
                    return rig
                except ValidationError:
                    print("Failed to validate pydantic model. Try again.")
                except ValueError:
                    print("Invalid choice. Try again.")

    def prompt_task_logic_input(self, folder: Optional[str] = None) -> TTaskLogic:
        _path = os.path.join(self.config_library_dir, folder, "*.json") if folder is not None else self._task_logic_dir
        available_files = glob.glob(_path)
        while True:
            try:
                path = self.pick_file_from_list(
                    available_files, prompt="Choose a task logic:", override_zero=(None, None)
                )
                if not os.path.isfile(path):
                    raise FileNotFoundError(f"File not found: {path}")
                task_logic = self.load_json_model(path, self.task_logic_schema)
                print(f"Using {path}.")
                return task_logic
            except ValidationError as validation_error:
                print(validation_error)
                print("Failed to validate pydantic model. Try again.")
            except ValueError:
                print("Invalid choice. Try again.")
            except FileNotFoundError:
                print("Invalid choice. Try again.")

    def prompt_visualizer_layout_input(self, folder_name: Optional[str] = None) -> Optional[str]:
        layout_schemas_path = (
            os.path.join(self.config_library_dir, folder_name, self.computer_name)
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
            except ValueError:
                print("Invalid choice. Try again.")

    def prompt_bonsai_config_input(self) -> dict[str, bool]:
        user_input = input("Press any key to continue or type 'bonsai' for advance settings")
        settings = {}
        if user_input == "bonsai":
            settings["is_editor_mode"] = self.prompt_yes_no_question("Run with editor mode?")
            if settings["is_editor_mode"]:
                settings["is_start_flag"] = self.prompt_yes_no_question("Run with start flag?")
        return settings

    def run(self) -> None:
        try:
            self._print_header()
            self._validate_dependencies()
            task_logic: TTaskLogic = self.prompt_task_logic_input()
            session: TSession = self.prompt_session_input()
            rig: TRig = self.prompt_rig_input()
            bonsai_visualizer_layout: Optional[str] = self.prompt_visualizer_layout_input()
            bonsai_config: Dict[str, bool] = self.prompt_bonsai_config_input()

            input("Press enter to launch Bonsai or Control+C to exit...")

            additional_properties = {
                "TaskLogicPath": os.path.abspath(self.save_temp_model(model=task_logic, folder=self.temp_dir)),
                "SessionPath": os.path.abspath(self.save_temp_model(model=session, folder=self.temp_dir)),
                "RigPath": os.path.abspath(self.save_temp_model(model=rig, folder=self.temp_dir)),
            }

            _date = session.date.strftime("%Y%m%dT%H%M%S")
            proc = open_bonsai_process(
                bonsai_exe=self.bonsai_executable,
                workflow_file=self.default_workflow,
                additional_properties=additional_properties,
                layout=bonsai_visualizer_layout,
                log_file_name=os.path.join(self.log_dir, f"{session.subject}_{session.experiment}_{_date}.log"),
                is_editor_mode=bonsai_config.get("is_editor_mode", True),
                is_start_flag=bonsai_config.get("is_start_flag", True),
                cwd=self._cwd,
            )
            print("Bonsai process running...")
            ret = proc.wait()
            print(f"Bonsai process finished with return code {ret}.")

        except KeyboardInterrupt:
            print("Exiting!")
            return

    def abspath(self, path: os.PathLike | str) -> str:
        """
        Returns the absolute path of the given file or directory.

        Args:
            path (os.PathLike | str): The path to the file or directory.

        Returns:
            str: The absolute path of the file or directory.

        """
        if not isinstance(path, str):
            path = str(path)
        return os.path.abspath(path)

    def make_folder_structure(self) -> None:
        try:
            self._make_folder(self.data_dir)
            self._make_folder(self._task_logic_dir)
            self._make_folder(self._rig_dir)
            self._make_folder(self._session_dir)
            self._make_folder(self._visualizer_layouts_dir)
        except OSError as e:
            print(f"Failed to create folder structure: {e}")

    @staticmethod
    def _make_folder(folder: os.PathLike | str) -> None:
        if not os.listdir(os.path.abspath(folder)):
            os.makedirs(folder)
