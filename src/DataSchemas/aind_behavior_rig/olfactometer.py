from enum import IntEnum
from typing import Dict, Literal

from aind_behavior_rig.base import OperationControlModel, RigCalibrationFullModel
from aind_data_schema.models.devices import OlfactometerChannel
from aind_data_schema.models.stimulus import OlfactometerChannelConfig
from pydantic import Field


class HarpOlfactometerChannel(IntEnum):
    """Harp Olfactometer available channel"""

    Channel0 = 0
    Channel1 = 1
    Channel2 = 2
    Channel3 = 3


class OlfactometerOperationControl(OperationControlModel):
    """Olfactometer operation control model that is used to run a calibration data acquisition workflow"""

    channel_config: Dict[HarpOlfactometerChannel, OlfactometerChannel] = Field(
        {}, description="Configuration of olfactometer channels"
    )
    stimulus_config: Dict[HarpOlfactometerChannel, OlfactometerChannelConfig] = Field(
        {}, description="Configuration of the odor stimuli"
    )
    full_flow_rate: float = Field(1000, ge=0, le=1000, description="Full flow rate of the olfactometer")
    target_stimulus_flow_rate: float = Field(100, ge=0, le=1000, description="Target flow rate of the odor stimuli")
    n_repeats_per_stimulus: int = Field(1, ge=1, description="Number of repeats per stimulus")
    time_on: float = Field(1, ge=0, description="Time (s) the valve is open during calibration", units="s")
    time_off: float = Field(1, ge=0, description="Time (s) the valve is close during calibration", units="s")


class OlfactometerCalibrationModel(RigCalibrationFullModel):
    schema_version: Literal["0.1.0"] = "0.1.0"
    operation_control: OlfactometerOperationControl
    calibration: Literal["Missing"] = "Missing"
