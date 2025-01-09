import logging
from enum import Enum, IntEnum
from typing import Dict, Literal, Optional

from pydantic import BaseModel, Field

from aind_behavior_services.calibration import Calibration
from aind_behavior_services.rig import (
    HarpOlfactometer,
)

logger = logging.getLogger(__name__)


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


class Olfactometer(HarpOlfactometer):
    calibration: Optional[OlfactometerCalibration] = Field(default=None, title="Calibration of the olfactometer")
