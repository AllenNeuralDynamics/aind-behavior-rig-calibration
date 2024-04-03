import os
import secrets
import git
from typing import Optional, Type
from pydantic import BaseModel
from aind_behavior_services import AindBehaviorRigModel, AindBehaviorSessionModel, AindBehaviorTaskLogicModel

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


class Launcher:
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
        remote_data_dir (Optional[os.PathLike | str]): The directory to log remote data.
        bonsai_executable (os.PathLike | str): The path to the Bonsai executable.
        workflow (os.PathLike | str): The path to the bonsai workflow file.
    """

    def __init__(
        self,
        rig_schema: Type[AindBehaviorRigModel],
        session_schema: Type[AindBehaviorSessionModel],
        task_logic_schema: Type[AindBehaviorTaskLogicModel],
        config_library_dir: os.PathLike | str = r"\\allen\aind\scratch\{task}\schemas",
        temp_dir: os.PathLike | str = "local/.temp",
        log_dir: os.PathLike | str = "local/.dump",
        remote_data_dir: Optional[os.PathLike | str] = None,
        bonsai_executable: os.PathLike | str = "bonsai/bonsai.exe",
        workflow: os.PathLike | str = "src/main.bonsai",
        repository: Optional[git.Repo] = None,
    ) -> None:
        """
        Initializes a new instance of the Launcher class.

        Parameters:
            rig_schema (Type[AindBehaviorRigModel]): The rig schema for the behavior services.
            session_schema (Type[AindBehaviorSessionModel]): The session schema for the behavior services.
            task_logic_schema (Type[AindBehaviorTaskLogicModel]): The task logic schema for the behavior services.
        """

        if repository is None:
            try:
                self.repository = git.Repo(search_parent_directories=True)
            except git.InvalidGitRepositoryError as e:
                raise e("Not a git repository. Please run from the root of the repository.") from e
        else:
            self.repository = repository

        self.rig_schema = rig_schema
        self.session_schema = session_schema
        self.task_logic_schema = task_logic_schema
        self.temp_dir = temp_dir
        self.log_dir = log_dir
        self.remote_data_dir = remote_data_dir
        self.bonsai_executable = bonsai_executable
        self.default_workflow = workflow
        if not isinstance(config_library_dir, str):
            config_library_dir = str(config_library_dir)
        self.config_library_dir = config_library_dir.format(task=task_logic_schema.__name__)
        self.computer_name = os.environ["COMPUTERNAME"]

        self._cwd = os.getcwd()

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
        print(_HEADER)
        print(f"TaskLogic Schema Version: {self.task_logic_schema.model_construct().schema_version}")
        print(f"Rig Schema Version: {self.rig_schema.model_construct().schema_version}")
        print(f"Session Schema Version: {self.session_schema.model_construct().schema_version}")
        print("-------------------------------")

    def save_temp_model(self, model: BaseModel, folder: Optional[os.PathLike | str]) -> str:
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
    def load_json_model(json_path: os.PathLike | str, model: BaseModel) -> BaseModel:
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
        if not (os.path.isdir(os.path.join(self.config_library_dir, "Rigs", self.computer_name))):
            raise FileNotFoundError(
                f"Rig configuration not found! Expected {os.path.join(self.config_library_dir, 'Rigs', self.computer_name)}."
            )
        if not (os.path.isfile(os.path.join(self.default_workflow))):
            raise FileNotFoundError(f"Bonsai workflow file not found! Expected {self.default_workflow}.")
