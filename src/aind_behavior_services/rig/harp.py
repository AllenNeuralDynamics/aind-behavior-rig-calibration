from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Annotated, List, Literal, Optional, Union

from pydantic import BaseModel, Field, field_validator
from typing_extensions import TypeAliasType

from aind_behavior_services.utils import get_fields_of_type

from ._base import Device, TRig


class HarpDeviceType(str, Enum):
    GENERIC = "generic"
    LOADCELLS = "loadcells"
    BEHAVIOR = "behavior"
    OLFACTOMETER = "olfactometer"
    CLOCKGENERATOR = "clockgenerator"
    CLOCKSYNCHRONIZER = "clocksynchronizer"
    TREADMILL = "treadmill"
    LICKOMETER = "lickometer"
    ANALOGINPUT = "analoginput"
    SOUNDCARD = "soundcard"
    SNIFFDETECTOR = "sniffdetector"
    CUTTLEFISH = "cuttlefish"
    STEPPERDRIVER = "stepperdriver"
    ENVIRONMENTSENSOR = "environmentsensor"
    WHITERABBIT = "whiterabbit"


class HarpDeviceGeneric(Device):
    who_am_i: Optional[int] = Field(default=None, le=9999, ge=0, description="Device WhoAmI")
    device_type: Literal[HarpDeviceType.GENERIC] = HarpDeviceType.GENERIC
    serial_number: Optional[str] = Field(default=None, description="Device serial number")
    port_name: str = Field(..., description="Device port name")


class ConnectedClockOutput(BaseModel):
    target_device: Optional[str] = Field(
        default=None, description="Optional device name to provide user additional information"
    )
    output_channel: int = Field(..., ge=0, description="Output channel")


def _assert_unique_output_channels(outputs: List[ConnectedClockOutput]) -> List[ConnectedClockOutput]:
    channels = set([ch.output_channel for ch in outputs])
    if len(channels) != len(outputs):
        raise ValueError("Output channels must be unique")
    return outputs


class HarpClockGenerator(HarpDeviceGeneric):
    device_type: Literal[HarpDeviceType.CLOCKGENERATOR] = HarpDeviceType.CLOCKGENERATOR
    who_am_i: Literal[1158] = 1158
    connected_clock_outputs: List[ConnectedClockOutput] = Field(default=[], description="Connected clock outputs")

    @field_validator("connected_clock_outputs")
    @classmethod
    def validate_connected_clock_outputs(cls, v: List[ConnectedClockOutput]) -> List[ConnectedClockOutput]:
        return _assert_unique_output_channels(v)


class HarpWhiteRabbit(HarpDeviceGeneric):
    device_type: Literal[HarpDeviceType.WHITERABBIT] = HarpDeviceType.WHITERABBIT
    who_am_i: Literal[1404] = 1404
    connected_clock_outputs: List[ConnectedClockOutput] = Field(default=[], description="Connected clock outputs")

    @field_validator("connected_clock_outputs")
    @classmethod
    def validate_connected_clock_outputs(cls, v: List[ConnectedClockOutput]) -> List[ConnectedClockOutput]:
        return _assert_unique_output_channels(v)


class HarpClockSynchronizer(HarpDeviceGeneric):
    device_type: Literal[HarpDeviceType.CLOCKSYNCHRONIZER] = HarpDeviceType.CLOCKSYNCHRONIZER
    who_am_i: Literal[1152] = 1152
    connected_clock_outputs: List[ConnectedClockOutput] = Field(default=[], description="Connected clock outputs")

    @field_validator("connected_clock_outputs")
    @classmethod
    def validate_connected_clock_outputs(cls, v: List[ConnectedClockOutput]) -> List[ConnectedClockOutput]:
        return _assert_unique_output_channels(v)


class HarpBehavior(HarpDeviceGeneric):
    device_type: Literal[HarpDeviceType.BEHAVIOR] = HarpDeviceType.BEHAVIOR
    who_am_i: Literal[1216] = 1216


class HarpSoundCard(HarpDeviceGeneric):
    device_type: Literal[HarpDeviceType.SOUNDCARD] = HarpDeviceType.SOUNDCARD
    who_am_i: Literal[1280] = 1280


class HarpLoadCells(HarpDeviceGeneric):
    device_type: Literal[HarpDeviceType.LOADCELLS] = HarpDeviceType.LOADCELLS
    who_am_i: Literal[1232] = 1232


class HarpOlfactometer(HarpDeviceGeneric):
    device_type: Literal[HarpDeviceType.OLFACTOMETER] = HarpDeviceType.OLFACTOMETER
    who_am_i: Literal[1140] = 1140


class HarpAnalogInput(HarpDeviceGeneric):
    device_type: Literal[HarpDeviceType.ANALOGINPUT] = HarpDeviceType.ANALOGINPUT
    who_am_i: Literal[1236] = 1236


class HarpLickometer(HarpDeviceGeneric):
    device_type: Literal[HarpDeviceType.LICKOMETER] = HarpDeviceType.LICKOMETER
    who_am_i: Literal[1400] = 1400


class HarpSniffDetector(HarpDeviceGeneric):
    device_type: Literal[HarpDeviceType.SNIFFDETECTOR] = HarpDeviceType.SNIFFDETECTOR
    who_am_i: Literal[1401] = 1401


class HarpTreadmill(HarpDeviceGeneric):
    device_type: Literal[HarpDeviceType.TREADMILL] = HarpDeviceType.TREADMILL
    who_am_i: Literal[1402] = 1402


class HarpCuttlefish(HarpDeviceGeneric):
    device_type: Literal[HarpDeviceType.CUTTLEFISH] = HarpDeviceType.CUTTLEFISH
    who_am_i: Literal[1403] = 1403


class HarpStepperDriver(HarpDeviceGeneric):
    device_type: Literal[HarpDeviceType.STEPPERDRIVER] = HarpDeviceType.STEPPERDRIVER
    who_am_i: Literal[1130] = 1130


class HarpEnvironmentSensor(HarpDeviceGeneric):
    device_type: Literal[HarpDeviceType.ENVIRONMENTSENSOR] = HarpDeviceType.ENVIRONMENTSENSOR
    who_am_i: Literal[1405] = 1405


_HarpDevice = Union[
    HarpBehavior,
    HarpOlfactometer,
    HarpClockGenerator,
    HarpAnalogInput,
    HarpLickometer,
    HarpTreadmill,
    HarpCuttlefish,
    HarpLoadCells,
    HarpSoundCard,
    HarpSniffDetector,
    HarpClockSynchronizer,
    HarpStepperDriver,
    HarpEnvironmentSensor,
    HarpWhiteRabbit,
    HarpDeviceGeneric,
]

if TYPE_CHECKING:
    HarpDevice = TypeAliasType(
        "HarpDevice",
        Annotated[_HarpDevice, Field(discriminator="device_type")],
    )
else:
    HarpDevice = _HarpDevice


def validate_harp_clock_output(rig: TRig) -> TRig:
    harp_devices = get_fields_of_type(rig, HarpDeviceGeneric)
    if len(harp_devices) < 2:
        return rig
    n_clock_targets = len(harp_devices) - 1
    clock_outputs = get_fields_of_type(rig, ConnectedClockOutput)
    if len(clock_outputs) != n_clock_targets:
        raise ValueError(f"Expected {n_clock_targets} clock outputs, got {len(clock_outputs)}")
    return rig
