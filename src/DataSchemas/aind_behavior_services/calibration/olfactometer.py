from enum import IntEnum, Enum
from typing import Dict, Literal, Optional

from aind_behavior_services.calibration import Calibration, CalibrationLogicModel
from pydantic import Field, BaseModel

__VERSION__ = "0.2.0"


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
    flow_rate_capacity: Literal[100, 1000] = Field(default=Literal[100], title="Flow capacity. mL/min")
    flow_rate: float = Field(
        default=100, le=100, title="Target flow rate. mL/min. If channel_type == CARRIER, this value is ignored."
    )
    odorant: Optional[str] = Field(None, title="Odorant name")
    odorant_dilution: Optional[float] = Field(None, title="Odorant dilution (%v/v)")


class OlfactometerOperationControl(CalibrationLogicModel):
    """Olfactometer operation control model that is used to run a calibration data acquisition workflow"""

    schema_version: Literal[__VERSION__] = __VERSION__
    describedBy: Literal[
        "https://raw.githubusercontent.com/AllenNeuralDynamics/Aind.Behavior.Services/main/src/DataSchemas/schemas/olfactometer_calibration.json"
    ] = "https://raw.githubusercontent.com/AllenNeuralDynamics/Aind.Behavior.Services/main/src/DataSchemas/schemas/olfactometer_calibration.json"
    channel_config: Dict[OlfactometerChannel, OlfactometerChannel] = Field(
        {}, description="Configuration of olfactometer channels"
    )
    full_flow_rate: float = Field(1000, ge=0, le=1000, description="Full flow rate of the olfactometer")
    n_repeats_per_stimulus: int = Field(1, ge=1, description="Number of repeats per stimulus")
    time_on: float = Field(1, ge=0, description="Time (s) the valve is open during calibration", units="s")
    time_off: float = Field(1, ge=0, description="Time (s) the valve is close during calibration", units="s")


class OlfaCalibrationInput(BaseModel):
    pass


class OlfaCalibrationOutput(BaseModel):
    pass


class OlfactometerCalibration(Calibration):
    """Olfactometer calibration class"""

    device_name: str = Field("Olfactometer", title="Device name", description="Name of the device being calibrated")
    input: OlfaCalibrationInput = Field(..., title="Input of the calibration")
    output: OlfaCalibrationOutput = Field(..., title="Output of the calibration")
    description: Literal["Calibration of the harp olfactometer device"] = "Calibration of the harp olfactometer device"
