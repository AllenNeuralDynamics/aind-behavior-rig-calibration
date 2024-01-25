from enum import IntEnum
from typing import Dict, Literal, Optional

from aind_behavior_services.calibration import OperationControlModel, RigCalibrationFullModel
from aind_data_schema.models.devices import OlfactometerChannel, Calibration
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
    n_repeats_per_stimulus: int = Field(1, ge=1, description="Number of repeats per stimulus")
    time_on: float = Field(1, ge=0, description="Time (s) the valve is open during calibration", units="s")
    time_off: float = Field(1, ge=0, description="Time (s) the valve is close during calibration", units="s")


class OlfactometerCalibration(Calibration):
    """Olfactometer calibration class"""

    device_name: str = Field(
        "Olfactometer", title="Device name", description="Must match a device name in rig/instrument"
    )
    description: Literal["Calibration of the harp olfactometer device"] = "Calibration of the harp olfactometer device"
    notes: Optional[str] = Field(None, title="Notes")


class OlfactometerCalibrationModel(RigCalibrationFullModel):
    schema_version: Literal["0.1.0"] = "0.1.0"
    describedBy: Literal[""] = ""
    operation_control: OlfactometerOperationControl
    calibration: Optional[OlfactometerCalibration] = Field(None, description="Calibration data")
