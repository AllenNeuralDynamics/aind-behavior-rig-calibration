from typing import Literal

import aind_behavior_services.base as base
from aind_data_schema.base import AindCoreModel
from pydantic import field_validator

__version__ = "0.1.0"


class AindBehaviorTaskLogicModel(AindCoreModel):
    schema_version: Literal[__version__] = __version__

    @field_validator("schema_version", mode="before")
    @classmethod
    def coerce_version(cls, v: str) -> str:
        return base.coerce_schema_version(cls, v)
