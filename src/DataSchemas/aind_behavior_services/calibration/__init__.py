from __future__ import annotations

import datetime
from typing import Optional

from aind_behavior_services.task_logic import AindBehaviorTaskLogicModel
from pydantic import BaseModel, Field


class CalibrationLogicModel(AindBehaviorTaskLogicModel):
    """Base class for all CalibrationLogicModel models"""

    pass


class Calibration(BaseModel):
    """Base class for all Calibration models. Stores calibration (meta)data."""

    device_name: str = Field(..., title="Device name", description="Name of the device being calibrated")
    input: Optional[BaseModel] = Field(default=None, title="Input data")
    output: Optional[BaseModel] = Field(default=None, title="Output data")
    date: Optional[datetime.datetime] = Field(default=None, title="Date")
    description: Optional[str] = Field(default=None, title="Brief description of what is being calibrated")
    notes: Optional[str] = Field(default=None, title="Notes")
