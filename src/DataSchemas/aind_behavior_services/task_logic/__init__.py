from typing import Optional

import aind_behavior_curriculum.task as curriculum_task
from aind_behavior_services.base import coerce_schema_version
from pydantic import Field, field_validator


class TaskParameters(curriculum_task.TaskParameters):
    rng_seed: Optional[float] = Field(default=None, description="Seed of the random number generator")
    stage_alias: Optional[str] = Field(default=None, description="Alias name used for the task stage")


class AindBehaviorTaskLogicModel(curriculum_task.Task):

    task_parameters: TaskParameters = Field(..., description="Parameters of the task logic", validate_default=True)

    @field_validator("version", mode="before")
    @classmethod
    def coerce_version(cls, v: str) -> str:
        return coerce_schema_version(cls, v)
