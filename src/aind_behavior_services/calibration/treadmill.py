import logging
from typing import ClassVar, List, Literal, Optional

from pydantic import BaseModel, Field, field_validator

from aind_behavior_services.calibration import Calibration
from aind_behavior_services.patterns import ValuePair
from aind_behavior_services.rig import HarpTreadmill

logger = logging.getLogger(__name__)


class TreadmillCalibrationInput(BaseModel):
    pass


class TreadmillCalibrationOutput(BaseModel):
    _BRAKE_OUTPUT_MAX: ClassVar[float] = 65535
    _BRAKE_OUTPUT_MIN: ClassVar[float] = 0
    _BRAKE_INPUT_MAX: ClassVar[float] = float("inf")
    _BRAKE_INPUT_MIN: ClassVar[float] = 0

    wheel_diameter: float = Field(default=15, ge=0, description="Wheel diameter")
    pulses_per_revolution: int = Field(default=28800, ge=1, description="Pulses per revolution")
    invert_direction: bool = Field(default=False, description="Invert direction")
    brake_lookup_calibration: List[ValuePair] = Field(
        ...,
        validate_default=True,
        min_length=2,
        description="Brake lookup calibration. Each pair of values define (input [torque], output [brake set-point U16])",
    )

    @field_validator("brake_lookup_calibration", mode="after")
    @classmethod
    def validate_brake_lookup_calibration(cls, value: List[ValuePair]) -> List[ValuePair]:
        for pair in value:
            if pair[0] < cls._BRAKE_INPUT_MIN or pair[0] > cls._BRAKE_INPUT_MAX:
                raise ValueError(f"Brake input value must be between {cls._BRAKE_INPUT_MIN} and {cls._BRAKE_INPUT_MAX}")
            if pair[1] < cls._BRAKE_OUTPUT_MIN or pair[1] > cls._BRAKE_OUTPUT_MAX:
                raise ValueError(
                    f"Brake output value must be between {cls._BRAKE_OUTPUT_MIN} and {cls._BRAKE_OUTPUT_MAX}"
                )
        return value


class TreadmillCalibration(Calibration):
    """Treadmill calibration class"""

    device_name: str = Field(
        default="Treadmill", title="Device name", description="Must match a device name in rig/instrument"
    )
    description: Literal["Calibration of the treadmill system"] = "Calibration of the treadmill system"
    input: TreadmillCalibrationInput = Field(..., title="Input of the calibration")
    output: TreadmillCalibrationOutput = Field(..., title="Output of the calibration.")


class Treadmill(HarpTreadmill):
    calibration: Optional[TreadmillCalibration] = Field(default=None, title="Calibration of the treadmill")
