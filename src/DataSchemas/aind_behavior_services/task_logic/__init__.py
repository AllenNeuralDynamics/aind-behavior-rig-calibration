from typing import Literal

from aind_behavior_services.base import SchemaVersionedModel, coerce_schema_version
from pydantic import field_validator

__version__ = "0.1.1"


class AindBehaviorTaskLogicModel(SchemaVersionedModel):
    schema_version: Literal[__version__] = __version__

    @field_validator("schema_version", mode="before")
    @classmethod
    def coerce_version(cls, v: str) -> str:
        return coerce_schema_version(cls, v)
