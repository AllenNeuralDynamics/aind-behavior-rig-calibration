import logging
import os
from typing import Callable, Optional, Tuple

from aind_behavior_services.db_utils import SubjectDataBase
from aind_behavior_services.rig import AindBehaviorRigModel
from aind_behavior_services.session import AindBehaviorSessionModel
from aind_behavior_services.task_logic import AindBehaviorTaskLogicModel


class UIHelper:
    _print: Callable[[str], None]
    _logger: logging.Logger

    def __init__(self, logger: logging.Logger, print_func: Callable[[str], None] = print):
        self._print = print_func
        self._logger = logger

    def prompt_pick_file_from_list(
        self,
        available_files: list[str],
        prompt: str = "Choose a file:",
        override_zero: Tuple[Optional[str], Optional[str]] = ("Enter manually", None),
    ) -> str:
        self._print(prompt)
        if override_zero[0] is not None:
            self._print(f"0: {override_zero[0]}")
        for i, file in enumerate(available_files):
            self._print(f"{i+1}: {os.path.split(file)[1]}")
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

    def prompt_yes_no_question(self, prompt: str) -> bool:
        while True:
            reply = input(prompt + " (Y\\N): ").upper()
            if reply == "Y" or reply == "1":
                return True
            elif reply == "N" or reply == "0":
                return False
            else:
                self._print("Invalid input. Please enter 'Y' or 'N'.")

    def choose_subject(self, subject_list: SubjectDataBase) -> str:
        subject = None
        while subject is None:
            try:
                subject = self.prompt_pick_file_from_list(
                    list(subject_list.subjects.keys()), prompt="Choose a subject:", override_zero=(None, None)
                )
            except ValueError as e:
                self._logger.error("Invalid choice. Try again. %s", e)
        return subject

    @staticmethod
    def prompt_get_notes() -> str:
        notes = str(input("Enter notes:"))
        return notes

    def print_header(
        self,
        task_logic_schema_model: type[AindBehaviorTaskLogicModel],
        rig_schema_model: type[AindBehaviorRigModel],
        session_schema_model: type[AindBehaviorSessionModel],
    ) -> None:
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
            f"TaskLogic ({task_logic_schema_model.__name__}) Schema Version: {task_logic_schema_model.model_construct().version}\n"
            f"Rig ({rig_schema_model.__name__}) Schema Version: {rig_schema_model.model_construct().version}\n"
            f"Session ({session_schema_model.__name__}) Schema Version: {session_schema_model.model_construct().version}\n"
            "-------------------------------"
        )

        self._logger.info(_str)
