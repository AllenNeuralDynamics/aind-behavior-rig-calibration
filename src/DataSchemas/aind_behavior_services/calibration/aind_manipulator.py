from typing import Annotated, Dict, List, Literal, Optional, Tuple
from enum import IntEnum

from aind_behavior_services.calibration import (
    CalibrationBase,
    OperationControlModel,
    RigCalibrationFullModel,
    RigCalibrationModel,
)
from pydantic import BaseModel, Field

__version__ = "0.1.0"

MIN_LIMIT = -1
MAX_LIMIT = 24000


class Axis(IntEnum):
    """Motor axis available"""

    NONE = 0
    Y1 = 1
    Y2 = 2
    X = 3
    Z = 4


class Vector4(BaseModel):
    x: float = Field(..., title="X coordinate")
    y1: float = Field(..., title="Y1 coordinate")
    y2: float = Field(..., title="Y2 coordinate")
    z: float = Field(..., title="Z coordinate")


class MicrostepResolution(IntEnum):
    MICROSTEP8 = 0
    MICROSTEP16 = 1
    MICROSTEP32 = 2
    MICROSTEP64 = 3


class MotorOperationMode(IntEnum):
    QUIET = 0
    DYNAMIC = 1


class AxisConfiguration(BaseModel):
    """Axis configuration"""

    axis: Axis = Field(..., title="Axis to be configured")
    step_acceleration_interval: int = Field(
        default=100,
        title="Acceleration",
        ge=2,
        le=2000,
        description="Acceleration of the step interval in microseconds",
    )
    step_interval: int = Field(
        default=100, title="Step interval", ge=100, le=20000, description="Step interval in microseconds."
    )
    microstep_resolution: MicrostepResolution = Field(
        default=MicrostepResolution.MICROSTEP8, title="Microstep resolution"
    )
    maximum_step_interval: int = Field(
        default=2000,
        ge=100,
        le=20000,
        title="Configures the time between step motor pulses (us) used when starting or stopping a movement",
    )
    motor_operation_mode: MotorOperationMode = Field(default=MotorOperationMode.QUIET, title="Motor operation mode")
    max_limit: int = Field(default=MAX_LIMIT, title="Maximum limit. A value of 0 disables this limit.")
    min_limit: int = Field(default=MIN_LIMIT, title="Minimum limit. A value of 0 disables this limit.")


class AindManipulatorCalibrationInput(RigCalibrationModel):
    full_step_to_mm: Vector4 = Field(default=(Vector4(x=0.010, y1=0.010, y2=0.010, z=0.010)), title="Full step to mm")


class AindManipulatorCalibrationOutput(RigCalibrationModel):
    pass


class AindManipulatorCalibration(CalibrationBase):
    """Load cells calibration class"""

    device_name: str = Field(
        "AindManipulator", title="Device name", description="Must match a device name in rig/instrument"
    )
    description: Literal["Calibration of the load cells system"] = "Calibration of the load cells system"
    input: AindManipulatorCalibrationInput = Field(default=..., title="Input of the calibration")
    output: AindManipulatorCalibrationOutput = Field(default=..., title="Output of the calibration.")
    notes: Optional[str] = Field(None, title="Notes")


class AindManipulatorOperationControl(OperationControlModel):
    AxesConfiguration: List[AxisConfiguration] = Field(
        default=[
            AxisConfiguration(axis=Axis.Y1),
            AxisConfiguration(axis=Axis.Y2),
            AxisConfiguration(axis=Axis.X),
            AxisConfiguration(axis=Axis.Z),
        ],
        title="Axes configuration. Only the axes that are configured will be enabled.",
        validate_default=True,
    )
    HomingOrder: List[Axis] = Field(
        default=[Axis.Y1, Axis.Y2, Axis.X, Axis.Z], title="Homing order", validate_default=True
    )
    InitialPosition: Vector4 = Field(default=Vector4(y1=0, y2=0, x=0, z=0), validate_default=True)


class AindManipulatorCalibrationModel(RigCalibrationFullModel):
    schema_version: Literal[__version__] = __version__
    describedBy: Literal[
        "https://raw.githubusercontent.com/AllenNeuralDynamics/Aind.Behavior.Services/main/src/DataSchemas/schemas/aind_manipulator_calibration.json"
    ] = "https://raw.githubusercontent.com/AllenNeuralDynamics/Aind.Behavior.Services/main/src/DataSchemas/schemas/aind_manipulator_calibration.json"
    operation_control: AindManipulatorOperationControl = Field(..., title="Operation control")
    calibration: Optional[AindManipulatorCalibration] = Field(default=None, description="Calibration data")
