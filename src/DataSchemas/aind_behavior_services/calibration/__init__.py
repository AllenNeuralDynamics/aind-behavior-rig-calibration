from __future__ import annotations

from datetime import datetime
from typing import Optional, TypeVar

from aind_data_schema.base import AindCoreModel, AindGeneric
from aind_data_schema.models.stimulus import Software
from pydantic import BaseModel, Field, RootModel


class RigCalibrationCoreModel(AindCoreModel):
    """Base class for all RigCalibrationCoreModel models"""


class RigCalibrationModel(AindGeneric, extra='forbid'):
    """Base class for all RigCalibrationModel models"""


class OperationControlModel(RigCalibrationModel):
    """Base class for all aind-behavior operation control models"""


class BonsaiWorkflow(Software):
    """Bonsai workflow"""


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
