from __future__ import annotations

from typing import Annotated, Dict, List, Literal, Optional

import numpy as np
from pydantic import BaseModel, Field
from sklearn.linear_model import LinearRegression

from aind_behavior_services.calibration import Calibration
from aind_behavior_services.rig import AindBehaviorRigModel
from aind_behavior_services.task_logic import AindBehaviorTaskLogicModel, TaskParameters

TASK_LOGIC_VERSION = "0.4.0"
RIG_VERSION = "0.0.0"

PositiveFloat = Annotated[float, Field(gt=0)]


class Measurement(BaseModel):
    """Input for water valve calibration class"""

    valve_open_interval: float = Field(
        ...,
        description="Time between two consecutive valve openings (s)",
        title="Valve open interval",
        gt=0,
    )
    valve_open_time: float = Field(
        ...,
        description="Valve open interval (s)",
        title="Valve open time",
        gt=0,
    )
    water_weight: List[PositiveFloat] = Field(
        ...,
        description="Weight of water delivered (g)",
        title="Water weight",
        min_length=1,
    )
    repeat_count: int = Field(..., ge=0, description="Number of times the valve opened.", title="Repeat count")


class WaterValveCalibrationInput(BaseModel):
    measurements: List[Measurement] = Field(default=[], description="List of measurements")

    def calibrate_output(self, input: Optional[WaterValveCalibrationInput] = None) -> WaterValveCalibrationOutput:
        """Calibrate the water valve delivery system by populating the output field"""
        # Calculate average volume per each measurement
        if input is None:
            input = self

        x_times = []
        y_weight = []

        for measurement in input.measurements:
            for weight in measurement.water_weight:
                x_times.append(measurement.valve_open_time)
                y_weight.append(weight / measurement.repeat_count)
        x_times = np.asarray(x_times)
        y_weight = np.asarray(y_weight)
        # Calculate the linear regression
        model = LinearRegression()
        model.fit(x_times.reshape(-1, 1), y_weight)
        return WaterValveCalibrationOutput(
            interval_average={x: np.mean(y_weight[x_times == x]) for x in np.unique(x_times)},
            slope=model.coef_[0],
            offset=model.intercept_,
            r2=model.score(x_times.reshape(-1, 1), y_weight),
            valid_domain=list(np.unique(x_times)),
        )


class WaterValveCalibrationOutput(BaseModel):
    """Output for water valve calibration class"""

    interval_average: Optional[Dict[PositiveFloat, PositiveFloat]] = Field(
        default=None,
        description="Dictionary keyed by measured valve interval and corresponding average single event volume.",
        title="Interval average",
    )
    slope: float = Field(
        ...,
        description="Slope of the linear regression : Volume(g) = Slope(g/s) * time(s) + offset(g)",
        title="Regression slope",
    )
    offset: float = Field(
        ...,
        description="Offset of the linear regression : Volume(g) = Slope(g/s) * time(s) + offset(g)",
        title="Regression offset",
    )
    r2: Optional[float] = Field(default=None, description="R2 metric from the linear model.", title="R2", ge=0, le=1)
    valid_domain: Optional[List[PositiveFloat]] = Field(
        default=None,
        description="The optional time-intervals the calibration curve was calculated on.",
        min_length=2,
        title="Valid domain",
    )


class WaterValveCalibration(Calibration):
    """Water valve calibration class"""

    device_name: str = Field(
        default="WaterValve", description="Name of the device being calibrated", title="Device name"
    )
    description: Literal["Calibration of the water valve delivery system"] = (
        "Calibration of the water valve delivery system"
    )
    input: WaterValveCalibrationInput = Field(..., title="Input of the calibration")
    output: WaterValveCalibrationOutput = Field(..., title="Output of the calibration.")


class CalibrationParameters(TaskParameters):
    valve_open_time: list[PositiveFloat] = Field(
        ...,
        min_length=1,
        description="An array with the times (s) the valve is open during calibration",
    )
    valve_open_interval: float = Field(
        default=0.2,
        description="Time between two consecutive valve openings (s)",
        title="Valve open interval",
        gt=0,
    )
    repeat_count: int = Field(
        default=200,
        ge=1,
        description="Number of times the valve opened per measure valve_open_time entry",
        title="Repeat count",
    )


class CalibrationLogic(AindBehaviorTaskLogicModel):
    """Olfactometer operation control model that is used to run a calibration data acquisition workflow"""

    name: str = Field(default="WaterValveCalibrationLogic", title="Task name")
    version: Literal[TASK_LOGIC_VERSION] = TASK_LOGIC_VERSION
    task_parameters: CalibrationParameters = Field(..., title="Task parameters", validate_default=True)


class CalibrationRig(AindBehaviorRigModel):
    version: Literal[RIG_VERSION] = RIG_VERSION
