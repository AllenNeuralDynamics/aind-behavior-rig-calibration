# Import core types
from datetime import datetime
from typing import List, Literal, Optional, Any

from pydantic import Field, field_validator

from aind_behavior_services.base import SchemaVersionedModel, coerce_schema_version

__version__ = "0.3.0"


class AindBehaviorSessionModel(SchemaVersionedModel):
    version: Literal[__version__] = __version__
    experiment: str = Field(..., description="Name of the experiment")
    experimenter: List[str] = Field(default=[], description="Name of the experimenter")
    date: datetime = Field(default_factory=datetime.now, description="Date of the experiment")
    root_path: str = Field(..., description="Root path where data will be logged")
    remote_path: Optional[str] = Field(
        default=None, description="Remote path where data will be attempted to be copied to after experiment is done"
    )
    subject: int = Field(..., description="Name of the subject")
    experiment_version: str = Field(..., description="Version of the experiment")
    notes: Optional[str] = Field(default=None, description="Notes about the experiment")
    commit_hash: Optional[str] = Field(default=None, description="Commit hash of the repository")
    allow_dirty_repo: bool = Field(default=False, description="Allow running from a dirty repository")
    skip_hardware_validation: bool = Field(default=False, description="Skip hardware validation")

    @field_validator("version", mode="before")
    @classmethod
    def coerce_version(cls, v: str) -> str:
        return coerce_schema_version(cls, v)

    @field_validator("subject", mode="before")
    @classmethod
    def coerce_subject_str_to_int(cls, v: Any) -> Any:
        return int(v) if v.isdecimal() else v