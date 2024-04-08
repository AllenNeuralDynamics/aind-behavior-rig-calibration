from enum import Enum, IntEnum
from typing import Dict, Literal, Optional

from aind_behavior_services.calibration import Calibration, CalibrationLogicModel
from aind_behavior_services.rig import AindBehaviorRigModel, HarpAnalogInput, HarpClockGenerator, HarpOlfactometer
from pydantic import BaseModel, Field

TASK_LOGIC_VERSION = "0.3.0"
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
    odorant: Optional[str] = Field(None, title="Odorant name")
    odorant_dilution: Optional[float] = Field(None, title="Odorant dilution (%v/v)")


class OlfactometerCalibrationInput(BaseModel):
    pass


class OlfactometerCalibrationOutput(BaseModel):
    pass


class OlfactometerCalibration(Calibration):
    """Olfactometer calibration class"""

    device_name: str = Field("Olfactometer", title="Device name", description="Name of the device being calibrated")
    description: Literal["Calibration of the harp olfactometer device"] = "Calibration of the harp olfactometer device"
    input: OlfactometerCalibrationInput = Field(..., title="Input of the calibration")
    output: OlfactometerCalibrationOutput = Field(..., title="Output of the calibration")


class CalibrationLogic(CalibrationLogicModel):
    """Olfactometer operation control model that is used to run a calibration data acquisition workflow"""

    schema_version: Literal[TASK_LOGIC_VERSION] = TASK_LOGIC_VERSION
    channel_config: Dict[OlfactometerChannel, OlfactometerChannelConfig] = Field(
        {}, description="Configuration of olfactometer channels"
    )
    full_flow_rate: float = Field(1000, ge=0, le=1000, description="Full flow rate of the olfactometer")
    n_repeats_per_stimulus: int = Field(1, ge=1, description="Number of repeats per stimulus")
    time_on: float = Field(1, ge=0, description="Time (s) the valve is open during calibration")
    time_off: float = Field(1, ge=0, description="Time (s) the valve is close during calibration")


class Olfactometer(HarpOlfactometer):
    calibration: OlfactometerCalibration = Field(..., title="Calibration of the olfactometer")


class CalibrationRig(AindBehaviorRigModel):
    schema_version: Literal[RIG_VERSION] = RIG_VERSION
    harp_olfactometer: Olfactometer = Field(..., title="Olfactometer device")
    harp_analog_input: HarpAnalogInput = Field(..., title="Analog input device")
    harp_clock_generator: HarpOlfactometer = Field(..., title="Clock generator device")
