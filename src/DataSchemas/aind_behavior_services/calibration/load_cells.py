from typing import Dict, List, Literal, Optional, Annotated

from aind_behavior_services.calibration import OperationControlModel, RigCalibrationFullModel, RigCalibrationModel
from aind_data_schema.models.devices import Calibration
from pydantic import Field, BaseModel

__version__ = "0.1.0"

LoadCellChannel = Annotated[int, Field(ge=0, le=7, description="Load cell channel number available")]


class LoadCellsCalibrationInput(RigCalibrationModel):
    pass


class LoadCellsCalibrationOutput(RigCalibrationModel):
    pass


class LoadCellsCalibration(Calibration):
    """Load cells calibration class"""

    device_name: str = Field(
        "LoadCells", title="Device name", description="Must match a device name in rig/instrument"
    )
    description: Literal["Calibration of the load cells system"] = (
        "Calibration of the load cells system"
    )
    input: LoadCellsCalibrationInput = Field(default=..., title="Input of the calibration")
    output: LoadCellsCalibrationOutput = Field(default=..., title="Output of the calibration.")
    notes: Optional[str] = Field(None, title="Notes")


class LoadCellsOperationControl(OperationControlModel):
    """Load cells operation control model that is used to run a calibration data acquisition workflow"""
    channels: List[LoadCellChannel] = Field(list(range(8)), description="List of channels to calibrate")
    offset_buffer_size: int = Field(
        default=200,
        description="Size of the buffer (in samples) acquired.",
        title="Buffer size",
        ge=1,
    )


class LoadCellsCalibrationModel(RigCalibrationFullModel):
    schema_version: Literal[__version__] = __version__
    describedBy: Literal[""] = ""
    operation_control: LoadCellsOperationControl = Field(..., title="Operation control")
    calibration: Optional[LoadCellsCalibration] = Field(None, description="Calibration data")
