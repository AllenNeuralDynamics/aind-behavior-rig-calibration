# Import core types
from datetime import datetime
from typing import Optional, Literal

# Import aind-datas-schema types
from aind_data_schema.base import AindCoreModel
from pydantic import Field

__version__ = "0.1.0"


class AindBehaviorSessionModel(AindCoreModel):
    schema_version: Literal[__version__] = Field(default=__version__)
    experiment: str = Field(..., description="Name of the experiment")
    date: datetime = Field(default_factory=datetime.now, description="Date of the experiment")
    root_path: str = Field(..., description="Root path where data will be logged")
    remote_path: Optional[str] = Field(
        default=None, description="Remote path where data will be attempted to be copied to after experiment is done"
    )
    subject: str = Field(..., description="Name of the subject")
    experiment_version: str = Field(..., description="Version of the experiment")
    rng_seed: Optional[float] = Field(default=None, description="Seed of the random number generator")
    notes: Optional[str] = Field(default=None, description="Notes about the experiment")
    commit_hash: Optional[str] = Field(default=None, description="Commit hash of the repository")
    allow_dirty_repo: bool = Field(default=False, description="Allow running from a dirty repository")
    skip_hardware_validation: bool = Field(default=False, description="Skip hardware validation")
