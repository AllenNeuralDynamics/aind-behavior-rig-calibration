from typing import Literal, Optional

from aind_behavior_services.base import SchemaVersionedModel, coerce_schema_version
from pydantic import field_validator, Field

__version__ = "0.1.1"


class AindBehaviorTaskLogicModel(SchemaVersionedModel):
    schema_version: Literal[__version__] = __version__
    rng_seed: Optional[float] = Field(default=None, description="Seed of the random number generator")

    @field_validator("schema_version", mode="before")
    @classmethod
    def coerce_version(cls, v: str) -> str:
        return coerce_schema_version(cls, v)
