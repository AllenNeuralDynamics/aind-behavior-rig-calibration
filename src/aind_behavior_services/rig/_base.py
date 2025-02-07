from __future__ import annotations

import os
from typing import Optional, TypeVar

from pydantic import BaseModel, Field

from aind_behavior_services.base import SchemaVersionedModel


class Device(BaseModel):
    device_type: str = Field(..., description="Device type")
    additional_settings: Optional[BaseModel] = Field(default=None, description="Additional settings")
    calibration: Optional[BaseModel] = Field(default=None, description="Calibration")


class AindBehaviorRigModel(SchemaVersionedModel):
    computer_name: str = Field(default_factory=lambda: os.environ["COMPUTERNAME"], description="Computer name")
    rig_name: str = Field(..., description="Rig name")


def _default_rig_name() -> str:
    if "RIG_NAME" not in os.environ:
        raise ValueError("RIG_NAME environment variable is not set. An explicit rig name must be provided.")
    else:
        return os.environ["RIG_NAME"]


TRig = TypeVar("TRig", bound=AindBehaviorRigModel)
