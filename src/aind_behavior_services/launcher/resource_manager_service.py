from __future__ import annotations

import logging
import shutil
from dataclasses import dataclass, field
from typing import Callable, List, Optional
import os

from aind_behavior_services.launcher._service import IService


class ResourceManager(IService):
    def __init__(
        self,
        logger: logging.Logger,
        constrains: Optional[List[Constraint]] = None,
    ) -> None:
        self.constraints = constrains or []
        self._logger = logger

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    def validate(self, *args, **kwargs) -> bool:
        return True

    def register(self, *args, **kwargs) -> None:
        pass

    def add_constraint(self, constraint: Constraint) -> None:
        self.constraints.append(constraint)

    def remove_constraint(self, constraint: Constraint) -> None:
        self.constraints.remove(constraint)

    def evaluate_constraints(self) -> bool:
        for constraint in self.constraints:
            if not constraint():
                self.logger.error(constraint.on_fail())
                return False
        return True


@dataclass(frozen=True)
class Constraint:
    name: str
    constraint: Callable[..., bool]
    args: List = field(default_factory=list)
    kwargs: dict = field(default_factory=dict)
    fail_msg_handler: Optional[Callable[..., str]] = field

    def __call__(self) -> bool | Exception:
        return self.constraint(*self.args, **self.kwargs)

    def on_fail(self) -> str:
        if self.fail_msg_handler:
            return self.fail_msg_handler(*self.args, **self.kwargs)
        return f"Constraint {self.name} failed."


def available_storage_constraint_factory(drive: str = "C:\\", min_bytes: float = 2e11) -> Constraint:
    return Constraint(
        name="available_storage",
        constraint=lambda drive, min_bytes: shutil.disk_usage(drive).free >= min_bytes,
        args=[],
        kwargs={"drive": drive, "min_bytes": min_bytes},
        fail_msg_handler=lambda drive,
        min_bytes: f"Drive {drive} does not have enough space. Minimum required: {min_bytes} bytes.",
    )


def remote_dir_exists_constraint_factory(dir_path: os.PathLike) -> Constraint:
    return Constraint(
        name="remote_dir_exists",
        constraint=lambda dir_path: os.path.exists(dir_path),
        args=[],
        kwargs={"dir_path": dir_path},
        fail_msg_handler=lambda dir_path: f"Directory {dir_path} does not exist.",
    )

