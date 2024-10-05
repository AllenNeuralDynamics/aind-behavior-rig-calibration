# Import core types
import datetime
from typing import List, Literal, Optional, Self

from pydantic import Field, field_validator, model_validator

import aind_behavior_services.utils
from aind_behavior_services.base import SchemaVersionedModel, coerce_schema_version

__version__ = "0.3.0"


class AindBehaviorSessionModel(SchemaVersionedModel):
    version: Literal[__version__] = __version__
    experiment: str = Field(..., description="Name of the experiment")
    experimenter: List[str] = Field(default=[], description="Name of the experimenter")
    date: datetime.datetime = Field(
        default_factory=aind_behavior_services.utils.utcnow, description="Date of the experiment", validate_default=True
    )  # TODO waiting for https://github.com/pydantic/pydantic/issues/9571
    root_path: str = Field(..., description="Root path where data will be logged")
    session_name: Optional[str] = Field(
        default=None, description="Name of the session. This will be used to create a folder in the root path."
    )
    subject: str = Field(..., description="Name of the subject")
    experiment_version: str = Field(..., description="Version of the experiment")
    notes: Optional[str] = Field(default=None, description="Notes about the experiment")
    commit_hash: Optional[str] = Field(default=None, description="Commit hash of the repository")
    allow_dirty_repo: bool = Field(default=False, description="Allow running from a dirty repository")
    skip_hardware_validation: bool = Field(default=False, description="Skip hardware validation")

    @field_validator("version", mode="before")
    @classmethod
    def coerce_version(cls, v: str, ctx) -> str:
        return coerce_schema_version(cls, v)

    @model_validator(mode="after")
    def generate_session_name_default(self) -> Self:
        if self.session_name is None:
            self.session_name = f"{self.subject}_{aind_behavior_services.utils.format_datetime(self.date)}"
        return self
