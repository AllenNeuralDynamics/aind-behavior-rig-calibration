from typing import Dict, List, Literal, Optional, Annotated

from aind_behavior_services.calibration import OperationControlModel, RigCalibrationFullModel, RigCalibrationModel
from aind_data_schema.models.devices import Calibration
from pydantic import Field, BaseModel

__version__ = "0.1.0"

PositiveFloat = Annotated[float, Field(gt=0)]


class Measurement(BaseModel):
    """Input for water valve calibration class"""

    valve_open_interval: float = Field(
        ...,
        description="Time between two consecutive valve openings (s)",
        title="Valve open interval",
        units="s",
        gt=0,
    )
    valve_open_time: float = Field(
        ...,
        description="Valve open interval (s)",
        title="Valve open time",
        units="s",
        gt=0,
    )
    water_weight: List[PositiveFloat] = Field(
        ...,
        description="Weight of water delivered (g)",
        title="Water weight",
        units="g",
        min_length=1,
    )
    repeat_count: int = Field(..., ge=0, description="Number of times the valve opened.", title="Repeat count")


class WaterValveCalibrationInput(BaseModel):
    measurements: List[Measurement] = Field(default=[], description="List of measurements")


class WaterValveCalibrationOutput(RigCalibrationModel):
    """Output for water valve calibration class"""

    interval_average: Optional[Dict[PositiveFloat, PositiveFloat]] = Field(
        None,
        description="Dictionary keyed by measured valve interval and corresponding average single event volume.",
        title="Interval average",
        units="s",
    )
    slope: float = Field(
        ...,
        description="Slope of the linear regression : Volume(g) = Slope(g/s) * time(s) + offset(g)",
        title="Regression slope",
        units="g/s",
    )
    offset: float = Field(
        ...,
        description="Offset of the linear regression : Volume(g) = Slope(g/s) * time(s) + offset(g)",
        title="Regression offset",
        units="g",
    )
    r2: float = Field(..., description="R2 metric from the linear model.", title="R2", ge=0, le=1)
    valid_domain: Optional[List[PositiveFloat]] = Field(
        None,
        description="The optional time-intervals the calibration curve was calculated on.",
        min_length=2,
        title="Valid domain",
        units="s",
    )


class WaterValveCalibration(Calibration):
    """Water valve calibration class"""

    device_name: str = Field(
        "WaterValve", title="Device name", description="Must match a device name in rig/instrument"
    )
    description: Literal["Calibration of the water valve delivery system"] = (
        "Calibration of the water valve delivery system"
    )
    input: WaterValveCalibrationInput = Field(default=..., title="Input of the calibration")
    output: WaterValveCalibrationOutput = Field(default=..., title="Output of the calibration.")
    notes: Optional[str] = Field(None, title="Notes")


class WaterValveOperationControl(OperationControlModel):
    """Olfactometer operation control model that is used to run a calibration data acquisition workflow"""

    valve_open_time: list[PositiveFloat] = Field(
        ...,
        min_length=1,
        description="An array with the times (s) the valve is open during calibration",
        units="s",
    )
    valve_open_interval: float = Field(
        0.2,
        description="Time between two consecutive valve openings (s)",
        title="Valve open interval",
        units="s",
        gt=0,
    )
    repeat_count: int = Field(
        200,
        ge=1,
        description="Number of times the valve opened per measure valve_open_time entry",
        title="Repeat count",
    )


class WaterValveCalibrationModel(RigCalibrationFullModel):
    schema_version: Literal[__version__] = __version__
    describedBy: Literal[""] = ""
    operation_control: WaterValveOperationControl
    calibration: Optional[WaterValveCalibration] = Field(None, description="Calibration data")
