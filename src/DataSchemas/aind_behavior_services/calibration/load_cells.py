from typing import Annotated, Dict, List, Literal, Optional, Tuple

from aind_behavior_services.calibration import CalibrationBase, CalibrationBaseModel, RigCalibrationFullModel
from aind_data_schema.models.units import MassUnit
from pydantic import BaseModel, Field

__VERSION__ = "0.2.0"

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


class LoadCellsCalibrationInput(CalibrationBaseModel):
    channels: Dict[LoadCellChannel, LoadCellCalibration] = Field(default={}, title="Load cells calibration data")
    weight_units: MassUnit = Field(default=MassUnit.G, title="Weight units")


class LoadCellsCalibrationOutput(CalibrationBaseModel):
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


class LoadCellsCalibration(CalibrationBase):
    """Load cells calibration class"""

    device_name: str = Field("LoadCells", title="Device name", description="Must match a device name in rig/instrument")
    description: Literal["Calibration of the load cells system"] = "Calibration of the load cells system"
    input: LoadCellsCalibrationInput = Field(default=..., title="Input of the calibration")
    output: LoadCellsCalibrationOutput = Field(default=..., title="Output of the calibration.")
    notes: Optional[str] = Field(None, title="Notes")

    def calibrate(self, input: Optional[LoadCellsCalibrationInput] = None):
        raise NotImplementedError


class LoadCellsOperationControl(CalibrationBaseModel):
    """Load cells operation control model that is used to run a calibration data acquisition workflow"""

    channels: List[LoadCellChannel] = Field(list(range(8)), description="List of channels to calibrate")
    offset_buffer_size: int = Field(
        default=200,
        description="Size of the buffer (in samples) acquired.",
        title="Buffer size",
        ge=1,
    )


class LoadCellsCalibrationModel(RigCalibrationFullModel):
    schema_version: Literal[__VERSION__] = __VERSION__
    describedBy: Literal[
        "https://raw.githubusercontent.com/AllenNeuralDynamics/Aind.Behavior.Services/main/src/DataSchemas/schemas/load_cells_calibration.json"
    ] = "https://raw.githubusercontent.com/AllenNeuralDynamics/Aind.Behavior.Services/main/src/DataSchemas/schemas/load_cells_calibration.json"
    operation_control: LoadCellsOperationControl = Field(..., title="Operation control")
    calibration: Optional[LoadCellsCalibration] = Field(None, description="Calibration data")
