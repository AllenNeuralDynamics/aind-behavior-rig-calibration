from __future__ import annotations

from typing import Optional

from aind_behavior_services.session import AindBehaviorSessionModel
from aind_data_schema.models.devices import Calibration
from pydantic import BaseModel, Field


class RigCalibrationFullModel(AindBehaviorSessionModel):
    """Base class for all RigCalibrationFullModel models"""

    operation_control: BaseModel = Field(..., title="Operation control")
    calibration: Optional[BaseModel] = Field(default=None, title="Calibration")


class CalibrationBaseModel(BaseModel):
    pass


class CalibrationBase(Calibration):
    """Base class for all calibration models"""
