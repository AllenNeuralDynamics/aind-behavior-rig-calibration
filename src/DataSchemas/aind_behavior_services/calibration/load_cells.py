from typing import Annotated, Dict, List, Literal, Tuple

from aind_behavior_services.calibration import Calibration
from aind_behavior_services.rig import AindBehaviorRigModel, HarpLoadCells
from aind_behavior_services.task_logic import AindBehaviorTaskLogicModel, TaskParameters
from pydantic import BaseModel, Field

TASK_LOGIC_VERSION = "0.4.0"
RIG_VERSION = "0.0.0"

LoadCellChannel = Annotated[int, Field(ge=0, le=7, description="Load cell channel number available")]

LoadCellOffset = Annotated[int, Field(ge=-255, le=255, description="Load cell offset value [-255, 255]")]


class LoadCellCalibration(BaseModel):
    measured_offset: Dict[LoadCellOffset, float] = Field(
        {}, title="Load cells offset. Each entry is expected to be in the format of: Channel : (offset, baseline)"
    )
    measured_weight: List[Tuple[float, float]] = Field(
        {},
        title="Load cells measured weight. Each entry is expected to be in the format of: (known weight(g), baseline)",
    )


class LoadCellsCalibrationInput(BaseModel):
    channels: Dict[LoadCellChannel, LoadCellCalibration] = Field(default={}, title="Load cells calibration data")


class LoadCellsCalibrationOutput(BaseModel):
    offset: Dict[LoadCellChannel, LoadCellOffset] = Field(
        default={lc: 0 for lc in range(8)}, validate_default=True, title="Load cells offset"
    )
    baseline: Dict[LoadCellChannel, float] = Field(
        default={lc: 0 for lc in range(8)},
        validate_default=True,
        title="Load cells baseline to be subtracted from the raw data after applying the offset.",
    )
    weight_lookup: Dict[LoadCellChannel, Tuple[float, float]] = Field(
        {}, validate_default=True, title="Load cells lookup calibration table for each channel: (weight, baseline)."
    )


class LoadCellsCalibration(Calibration):
    """Load cells calibration class"""

    device_name: str = Field("LoadCells", title="Device name", description="Must match a device name in rig/instrument")
    description: Literal["Calibration of the load cells system"] = "Calibration of the load cells system"
    input: LoadCellsCalibrationInput = Field(default=..., title="Input of the calibration")
    output: LoadCellsCalibrationOutput = Field(default=..., title="Output of the calibration.")


class CalibrationParameters(TaskParameters):
    channels: List[LoadCellChannel] = Field(list(range(8)), description="List of channels to calibrate")
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


class CalibrationRig(AindBehaviorRigModel):
    version: Literal[RIG_VERSION] = RIG_VERSION
    load_cells: HarpLoadCells = Field(..., title="Load Cells acquisition device")
