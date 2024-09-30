import glob
import logging
import os
import subprocess
from pathlib import Path
from typing import Dict, Optional, Self

from aind_behavior_services.launcher._service import IService
from aind_behavior_services.launcher.ui_helper import UIHelper
from aind_behavior_services.utils import run_bonsai_process


class App(IService):
    def __init__(self, *args, logger: Optional[logging.Logger] = None, **kwargs) -> None:
        self._logger = logger

    def validate(self, *args, **kwargs) -> bool:
        raise NotImplementedError

    @property
    def logger(self) -> logging.Logger:
        if self._logger is None:
            raise ValueError("Logger not set")
        return self._logger

    @logger.setter
    def logger(self, logger: logging.Logger) -> None:
        if self._logger is not None:
            raise ValueError("Logger already set")
        self._logger = logger


class BonsaiApp(App):
    executable: os.PathLike
    workflow: os.PathLike
    is_editor_mode: bool
    is_start_flag: bool
    layout: Optional[os.PathLike | str]
    layout_directory: Optional[os.PathLike]
    additional_properties: Optional[Dict[str, str]]
    cwd: Optional[os.PathLike]
    timeout: Optional[float]
    print_cmd: bool
    _result: Optional[subprocess.CompletedProcess]

    def __init__(
        self,
        workflow: os.PathLike,
        executable: os.PathLike = Path("./bonsai/bonsai.exe"),
        /,
        is_editor_mode: bool = True,
        is_start_flag: bool = True,
        layout: Optional[os.PathLike] = None,
        layout_dir: Optional[os.PathLike] = None,
        additional_properties: Optional[Dict[str, str]] = None,
        cwd: Optional[os.PathLike] = None,
        timeout: Optional[float] = None,
        logger: Optional[logging.Logger] = None,
        print_cmd: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(logger)
        self.executable = Path(executable).resolve()
        self.workflow = Path(workflow).resolve()
        self.is_editor_mode = is_editor_mode
        self.is_start_flag = is_start_flag if not self.is_editor_mode else True
        self.layout = layout
        self.layout_directory = layout_dir
        self.additional_properties = additional_properties or {}
        self.cwd = cwd
        self.timeout = timeout
        self.print_cmd = print_cmd
        self._result = None

    @property
    def result(self) -> subprocess.CompletedProcess:
        if self._result is None:
            raise RuntimeError("The app has not been run yet.")
        return self._result

    def validate(self, *args, **kwargs) -> bool:
        if not Path(self.executable).exists():
            raise FileNotFoundError(f"Executable not found: {self.executable}")
        if not Path(self.workflow).exists():
            raise FileNotFoundError(f"Workflow file not found: {self.workflow}")
        if self.layout and not Path(self.layout).exists():
            raise FileNotFoundError(f"Layout file not found: {self.layout}")
        if self.layout_directory and not Path(self.layout_directory).exists():
            raise FileNotFoundError(f"Layout directory not found: {self.layout_directory}")
        return True

    def run(self) -> subprocess.CompletedProcess:
        self.validate()

        if self.is_editor_mode:
            self.logger.warning("Bonsai is running in editor mode. Cannot assert successful completion.")
        self.logger.info("Bonsai process running...")
        proc = run_bonsai_process(
            workflow_file=self.workflow,
            bonsai_exe=self.executable,
            is_editor_mode=self.is_editor_mode,
            is_start_flag=self.is_start_flag,
            layout=self.layout,
            additional_properties=self.additional_properties,
            cwd=self.cwd,
            timeout=self.timeout,
            print_cmd=self.print_cmd,
        )
        self._result = proc
        self.logger.info("Bonsai process completed.")
        return proc

    def output_from_result(self, allow_stderr: Optional[bool]) -> Self:
        proc = self.result
        try:
            proc.check_returncode()
        except subprocess.CalledProcessError as e:
            self._log_process_std_output("Bonsai", proc)
            raise e
        else:
            self.logger.info("Result from bonsai process is valid.")
            self._log_process_std_output("Bonsai", proc)

            if len(proc.stdout) > 0:
                self.logger.error("Bonsai process finished with errors.")
                if allow_stderr is None:
                    allow_stderr = UIHelper(self.logger, print).prompt_yes_no_question(
                        "Would you like to see the error message?"
                    )
                if allow_stderr is False:
                    raise subprocess.CalledProcessError(1, proc.args)
        return self

    def prompt_visualizer_layout_input(
        self,
        directory: Optional[os.PathLike] = None,
    ) -> Optional[str | os.PathLike]:
        # This could use some refactoring. The bonsai CLI logic is:
        # 1. If a layout is provided, use that.
        # 2. If a layout is not provided, use the default layout
        # 3. if the layout is passed as "" (empty string) no layout is used.
        layout_schemas_path = directory if directory is not None else self.layout_directory
        available_layouts = glob.glob(os.path.join(str(layout_schemas_path), "*.bonsai.layout"))
        picked: Optional[str | os.PathLike] = None
        has_pick = False
        while has_pick is False:
            try:
                available_layouts.insert(0, "None")
                picked = UIHelper(self.logger, print).prompt_pick_file_from_list(
                    available_layouts, prompt="Pick a visualizer layout:", override_zero=("Default", None)
                )
                if picked == "None":
                    picked = ""
            except ValueError as e:
                self.logger.error("Invalid choice. Try again. %s", e)
            has_pick = True
        self.layout = picked
        return self.layout

    def _log_process_std_output(self, process_name: str, proc: subprocess.CompletedProcess) -> None:
        if len(proc.stdout) > 0:
            self.logger.info("%s full stdout dump: \n%s", process_name, proc.stdout)
        if len(proc.stderr) > 0:
            self.logger.error("%s full stderr dump: \n%s", process_name, proc.stderr)
