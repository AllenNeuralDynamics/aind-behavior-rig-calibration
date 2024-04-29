from typing import Optional

from aind_behavior_services.base import SchemaVersionedModel, coerce_schema_version
from pydantic import Field, field_validator


class AindBehaviorTaskLogicModel(SchemaVersionedModel):
    rng_seed: Optional[float] = Field(default=None, description="Seed of the random number generator")
    name: Optional[str] = Field(default=None, description="Optional name of the task or stage")

    @field_validator("schema_version", mode="before")
    @classmethod
    def coerce_version(cls, v: str) -> str:
        return coerce_schema_version(cls, v)
