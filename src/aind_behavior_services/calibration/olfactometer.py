from enum import Enum, IntEnum
from typing import Dict, Literal, Optional

from pydantic import BaseModel, Field

from aind_behavior_services.calibration import Calibration
from aind_behavior_services.rig import (
    AindBehaviorRigModel,
    HarpAnalogInput,
    HarpClockGenerator,
    HarpOlfactometer,
)
from aind_behavior_services.task_logic import AindBehaviorTaskLogicModel, TaskParameters

TASK_LOGIC_VERSION = "0.4.0"
RIG_VERSION = "0.0.0"


class OlfactometerChannel(IntEnum):
    """Harp Olfactometer available channel"""

    Channel0 = 0
    Channel1 = 1
    Channel2 = 2
    Channel3 = 3


class OlfactometerChannelType(str, Enum):
    """Channel type"""

    ODOR = "Odor"
    CARRIER = "Carrier"


class OlfactometerChannelConfig(BaseModel):
    channel_index: int = Field(..., title="Channel index")
    channel_type: OlfactometerChannelType = Field(default=OlfactometerChannelType.ODOR, title="Channel type")
    flow_rate_capacity: Literal[100, 1000] = Field(default=100, title="Flow capacity. mL/min")
    flow_rate: float = Field(
        default=100, le=100, title="Target flow rate. mL/min. If channel_type == CARRIER, this value is ignored."
    )
    odorant: Optional[str] = Field(default=None, title="Odorant name")
    odorant_dilution: Optional[float] = Field(default=None, title="Odorant dilution (%v/v)")


class OlfactometerCalibrationInput(BaseModel):
    channel_config: Dict[OlfactometerChannel, OlfactometerChannelConfig] = Field(
        default={}, description="Configuration of olfactometer channels"
    )


class OlfactometerCalibrationOutput(BaseModel):
    pass


class OlfactometerCalibration(Calibration):
    """Olfactometer calibration class"""

    device_name: str = Field(
        default="Olfactometer", title="Device name", description="Name of the device being calibrated"
    )
    description: Literal["Calibration of the harp olfactometer device"] = "Calibration of the harp olfactometer device"
    input: OlfactometerCalibrationInput = Field(..., title="Input of the calibration")
    output: OlfactometerCalibrationOutput = Field(..., title="Output of the calibration")


class CalibrationParameters(TaskParameters):
    channel_config: Dict[OlfactometerChannel, OlfactometerChannelConfig] = Field(
        default={}, description="Configuration of olfactometer channels"
    )
    full_flow_rate: float = Field(default=1000, ge=0, le=1000, description="Full flow rate of the olfactometer")
    n_repeats_per_stimulus: int = Field(default=1, ge=1, description="Number of repeats per stimulus")
    time_on: float = Field(default=1, ge=0, description="Time (s) the valve is open during calibration")
    time_off: float = Field(default=1, ge=0, description="Time (s) the valve is close during calibration")


class CalibrationLogic(AindBehaviorTaskLogicModel):
    """Olfactometer operation control model that is used to run a calibration data acquisition workflow"""

    name: str = Field(default="OlfactometerCalibrationLogic", title="Task name")
    version: Literal[TASK_LOGIC_VERSION] = TASK_LOGIC_VERSION
    task_parameters: CalibrationParameters = Field(..., title="Task parameters", validate_default=True)


class Olfactometer(HarpOlfactometer):
    calibration: Optional[OlfactometerCalibration] = Field(default=None, title="Calibration of the olfactometer")


class CalibrationRig(AindBehaviorRigModel):
    version: Literal[RIG_VERSION] = RIG_VERSION
    harp_olfactometer: Olfactometer = Field(..., title="Olfactometer device")
    harp_analog_input: HarpAnalogInput = Field(..., title="Analog input device")
    harp_clock_generator: HarpClockGenerator = Field(..., title="Clock generator device")
