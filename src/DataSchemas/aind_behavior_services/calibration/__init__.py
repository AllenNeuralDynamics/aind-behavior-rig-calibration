from __future__ import annotations

from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Any, Optional, TypeVar

from aind_data_schema.base import AindCoreModel, AindGeneric
from aind_data_schema.models.devices import Calibration
from aind_data_schema.models.stimulus import Software
from pydantic import BaseModel, Field, RootModel, model_validator


class RigCalibrationCoreModel(AindCoreModel):
    """Base class for all RigCalibrationCoreModel models"""


class RigCalibrationModel(AindGeneric, extra="forbid"):
    """Base class for all RigCalibrationModel models"""


class OperationControlModel(RigCalibrationModel):
    """Base class for all aind-behavior operation control models"""


class BonsaiWorkflow(Software):
    """Bonsai workflow"""


class CalibrationBase(Calibration, metaclass=ABCMeta):
    """Base class for all calibration models"""

    @abstractmethod
    def calibrate(self, input: Optional[AindGeneric] = None) -> AindGeneric:
        raise NotImplementedError


class RigCalibrationFullModel(RigCalibrationCoreModel):
    """Base class for all RigCalibrationFullModel models"""

    operation_control: OperationControlModel = Field(..., title="Operation control")
    calibration: Optional[BaseModel] = Field(None, title="Calibration")
    rootPath: str = Field(..., description="Root path of the experiment")
    date: datetime = Field(default_factory=datetime.now, title="Date")
    notes: str = Field("", title="Notes")
    experiment: str = Field("Calibration", description="Name of the experiment")
    experimenter: str = Field("Experimenter", description="Name of the subject")
    allowDirty: bool = Field(False, description="Allow code to run from dirty repository")
    remoteDataPath: Optional[str] = Field(
        default=None,
        description="Path to remote data. If null, no attempt to copy data will be made",
    )
    rngSeed: int = Field(
        0,
        description="Seed of the random number generator. If 0 it will be randomized.",
    )
    commitHash: Optional[str] = Field(None, description="Commit hash of the repository")
