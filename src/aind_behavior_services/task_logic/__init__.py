from typing import Literal, Optional

import aind_behavior_curriculum.task as curriculum_task
from pydantic import Field, field_validator

from aind_behavior_services import __version__ as pkg_version
from aind_behavior_services.base import SEMVER_REGEX, coerce_schema_version


class TaskParameters(curriculum_task.TaskParameters):
    rng_seed: Optional[float] = Field(default=None, description="Seed of the random number generator")
    aind_behavior_services_pkg_version: Literal[pkg_version] = Field(
        default=pkg_version, pattern=SEMVER_REGEX, title="aind_behavior_services package version", frozen=True
    )

    @field_validator("aind_behavior_services_pkg_version", mode="before", check_fields=False)
    @classmethod
    def coerce_version(cls, v: str, ctx) -> str:
        return coerce_schema_version(cls, v, ctx.field_name)


# This class should be inherited from but do not add extra parameters. Instead, add them to TaskParameters
class AindBehaviorTaskLogicModel(curriculum_task.Task):
    task_parameters: TaskParameters = Field(..., description="Parameters of the task logic", validate_default=True)
    version: str = Field(..., pattern=curriculum_task.SEMVER_REGEX, description="task schema version")

    @field_validator("version", mode="before", check_fields=False)
    @classmethod
    def coerce_version(cls, v: str) -> str:
        return coerce_schema_version(cls, v)
