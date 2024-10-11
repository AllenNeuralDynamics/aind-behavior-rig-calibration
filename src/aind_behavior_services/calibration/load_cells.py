from typing import Annotated, List, Literal, Optional

from pydantic import BaseModel, Field, field_validator

from aind_behavior_services.calibration import Calibration
from aind_behavior_services.rig import AindBehaviorRigModel, HarpLoadCells
from aind_behavior_services.task_logic import AindBehaviorTaskLogicModel, TaskParameters

TASK_LOGIC_VERSION = "0.4.0"
RIG_VERSION = "0.0.0"

LoadCellChannel = Annotated[int, Field(ge=0, le=7, description="Load cell channel number available")]

LoadCellOffset = Annotated[int, Field(ge=-255, le=255, description="Load cell offset value [-255, 255]")]


class MeasuredOffset(BaseModel):
    offset: LoadCellOffset = Field(..., description="The applied offset resistor value[-255, 255]")
    baseline: float = Field(..., description="The measured baseline value")


class MeasuredWeight(BaseModel):
    weight: float = Field(..., description="The applied weight in grams")
    baseline: float = Field(..., description="The measured baseline value")


class LoadCellCalibrationInput(BaseModel):
    channel: LoadCellChannel = Field(..., title="Load cell channel number")
    offset_measurement: List[MeasuredOffset] = Field(
        default=[],
        title="Load cell offset calibration data",
        validate_default=True,
    )
    weight_measurement: List[MeasuredWeight] = Field(
        default=[],
        title="Load cell weight calibration data",
        validate_default=True,
    )


class LoadCellsCalibrationInput(BaseModel):
    channels: List[LoadCellCalibrationInput] = Field(
        default=[], title="Load cells calibration data", validate_default=True
    )

    @field_validator("channels", mode="after")
    @classmethod
    def ensure_unique_channels(cls, values: List[LoadCellCalibrationInput]) -> List[LoadCellCalibrationInput]:
        channels = [c.channel for c in values]
        if len(channels) != len(set(channels)):
            raise ValueError("Channels must be unique.")
        return values


class LoadCellCalibrationOutput(BaseModel):
    channel: LoadCellChannel
    offset: Optional[LoadCellOffset] = Field(default=None, title="Load cell offset")
    baseline: Optional[float] = Field(default=None, title="Load cell baseline")
    weight_lookup: List[MeasuredWeight] = Field(default=[], title="Load cell weight lookup calibration table")


class LoadCellsCalibrationOutput(BaseModel):
    channels: List[LoadCellCalibrationOutput] = Field(
        default=[], title="Load cells calibration output", validate_default=True
    )

    @field_validator("channels", mode="after")
    @classmethod
    def ensure_unique_channels(cls, values: List[LoadCellCalibrationOutput]) -> List[LoadCellCalibrationOutput]:
        channels = [c.channel for c in values]
        if len(channels) != len(set(channels)):
            raise ValueError("Channels must be unique.")
        return values


class LoadCellsCalibration(Calibration):
    """Load cells calibration class"""

    device_name: str = Field(
        default="LoadCells", title="Device name", description="Must match a device name in rig/instrument"
    )
    description: Literal["Calibration of the load cells system"] = "Calibration of the load cells system"
    input: LoadCellsCalibrationInput = Field(..., title="Input of the calibration")
    output: LoadCellsCalibrationOutput = Field(..., title="Output of the calibration.")


class CalibrationParameters(TaskParameters):
    channels: List[LoadCellChannel] = Field(default=list(range(8)), description="List of channels to calibrate")
    offset_buffer_size: int = Field(
        default=200,
        description="Size of the buffer (in samples) acquired.",
        title="Buffer size",
        ge=1,
    )


class CalibrationLogic(AindBehaviorTaskLogicModel):
    """Load cells operation control model that is used to run a calibration data acquisition workflow"""

    name: str = Field(default="LoadCellsCalibrationLogic", title="Task name")
    version: Literal[TASK_LOGIC_VERSION] = TASK_LOGIC_VERSION
    task_parameters: CalibrationParameters = Field(..., title="Task parameters", validate_default=True)


class LoadCells(HarpLoadCells):
    calibration: Optional[LoadCellsCalibration] = Field(default=None, title="Calibration of the load cells")


class CalibrationRig(AindBehaviorRigModel):
    version: Literal[RIG_VERSION] = RIG_VERSION
    load_cells: LoadCells = Field(..., title="Load Cells acquisition device")
