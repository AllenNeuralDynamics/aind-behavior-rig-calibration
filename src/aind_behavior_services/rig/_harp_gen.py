# Auto-generated code. Do not edit manually.

from typing import TYPE_CHECKING, Annotated, List, Literal, Optional, Union

from pydantic import BaseModel, Field, field_validator
from typing_extensions import TypeAliasType

from ._base import Device


class _HarpDeviceBase(Device):
    who_am_i: Optional[int] = Field(default=None, le=9999, ge=0, description="Device WhoAmI")
    device_type: str
    serial_number: Optional[str] = Field(default=None, description="Device serial number")
    port_name: str = Field(..., description="Device port name")


class HarpDeviceGeneric(_HarpDeviceBase):
    device_type: Literal["Generic"] = "Generic"


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


class HarpUSBHub(_HarpDeviceBase):
    device_type: Literal["USBHub"] = "USBHub"
    who_am_i: Literal[256] = 256


class HarpPoke(_HarpDeviceBase):
    device_type: Literal["Poke"] = "Poke"
    who_am_i: Literal[1024] = 1024


class HarpMultiPwmGenerator(_HarpDeviceBase):
    device_type: Literal["MultiPwmGenerator"] = "MultiPwmGenerator"
    who_am_i: Literal[1040] = 1040


class HarpWear(_HarpDeviceBase):
    device_type: Literal["Wear"] = "Wear"
    who_am_i: Literal[1056] = 1056


class HarpWearBaseStationGen2(_HarpDeviceBase):
    device_type: Literal["WearBaseStationGen2"] = "WearBaseStationGen2"
    who_am_i: Literal[1058] = 1058


class HarpDriver12Volts(_HarpDeviceBase):
    device_type: Literal["Driver12Volts"] = "Driver12Volts"
    who_am_i: Literal[1072] = 1072


class HarpLedController(_HarpDeviceBase):
    device_type: Literal["LedController"] = "LedController"
    who_am_i: Literal[1088] = 1088


class HarpSynchronizer(_HarpDeviceBase):
    device_type: Literal["Synchronizer"] = "Synchronizer"
    who_am_i: Literal[1104] = 1104


class HarpInputExpander(_HarpDeviceBase):
    device_type: Literal["InputExpander"] = "InputExpander"
    who_am_i: Literal[1106] = 1106


class HarpOutputExpander(_HarpDeviceBase):
    device_type: Literal["OutputExpander"] = "OutputExpander"
    who_am_i: Literal[1108] = 1108


class HarpSimpleAnalogGenerator(_HarpDeviceBase):
    device_type: Literal["SimpleAnalogGenerator"] = "SimpleAnalogGenerator"
    who_am_i: Literal[1121] = 1121


class HarpStepperDriver(_HarpDeviceBase):
    device_type: Literal["StepperDriver"] = "StepperDriver"
    who_am_i: Literal[1130] = 1130


class HarpArchimedes(_HarpDeviceBase):
    device_type: Literal["Archimedes"] = "Archimedes"
    who_am_i: Literal[1136] = 1136


class HarpOlfactometer(_HarpDeviceBase):
    device_type: Literal["Olfactometer"] = "Olfactometer"
    who_am_i: Literal[1140] = 1140


class HarpClockSynchronizer(_HarpDeviceBase):
    device_type: Literal["ClockSynchronizer"] = "ClockSynchronizer"
    who_am_i: Literal[1152] = 1152
    connected_clock_outputs: List[ConnectedClockOutput] = Field(default=[], description="Connected clock outputs")

    @field_validator("connected_clock_outputs")
    @classmethod
    def validate_connected_clock_outputs(cls, v: List[ConnectedClockOutput]) -> List[ConnectedClockOutput]:
        return _assert_unique_output_channels(v)


class HarpTimestampGeneratorGen1(_HarpDeviceBase):
    device_type: Literal["TimestampGeneratorGen1"] = "TimestampGeneratorGen1"
    who_am_i: Literal[1154] = 1154
    connected_clock_outputs: List[ConnectedClockOutput] = Field(default=[], description="Connected clock outputs")

    @field_validator("connected_clock_outputs")
    @classmethod
    def validate_connected_clock_outputs(cls, v: List[ConnectedClockOutput]) -> List[ConnectedClockOutput]:
        return _assert_unique_output_channels(v)


class HarpTimestampGeneratorGen3(_HarpDeviceBase):
    device_type: Literal["TimestampGeneratorGen3"] = "TimestampGeneratorGen3"
    who_am_i: Literal[1158] = 1158
    connected_clock_outputs: List[ConnectedClockOutput] = Field(default=[], description="Connected clock outputs")

    @field_validator("connected_clock_outputs")
    @classmethod
    def validate_connected_clock_outputs(cls, v: List[ConnectedClockOutput]) -> List[ConnectedClockOutput]:
        return _assert_unique_output_channels(v)


class HarpCameraController(_HarpDeviceBase):
    device_type: Literal["CameraController"] = "CameraController"
    who_am_i: Literal[1168] = 1168


class HarpCameraControllerGen2(_HarpDeviceBase):
    device_type: Literal["CameraControllerGen2"] = "CameraControllerGen2"
    who_am_i: Literal[1170] = 1170


class HarpPyControlAdapter(_HarpDeviceBase):
    device_type: Literal["PyControlAdapter"] = "PyControlAdapter"
    who_am_i: Literal[1184] = 1184


class HarpBehavior(_HarpDeviceBase):
    device_type: Literal["Behavior"] = "Behavior"
    who_am_i: Literal[1216] = 1216


class HarpVestibularH1(_HarpDeviceBase):
    device_type: Literal["VestibularH1"] = "VestibularH1"
    who_am_i: Literal[1224] = 1224


class HarpVestibularH2(_HarpDeviceBase):
    device_type: Literal["VestibularH2"] = "VestibularH2"
    who_am_i: Literal[1225] = 1225


class HarpLoadCells(_HarpDeviceBase):
    device_type: Literal["LoadCells"] = "LoadCells"
    who_am_i: Literal[1232] = 1232


class HarpAnalogInput(_HarpDeviceBase):
    device_type: Literal["AnalogInput"] = "AnalogInput"
    who_am_i: Literal[1236] = 1236


class HarpRgbArray(_HarpDeviceBase):
    device_type: Literal["RgbArray"] = "RgbArray"
    who_am_i: Literal[1248] = 1248


class HarpFlyPad(_HarpDeviceBase):
    device_type: Literal["FlyPad"] = "FlyPad"
    who_am_i: Literal[1200] = 1200


class HarpSoundCard(_HarpDeviceBase):
    device_type: Literal["SoundCard"] = "SoundCard"
    who_am_i: Literal[1280] = 1280


class HarpSyringePump(_HarpDeviceBase):
    device_type: Literal["SyringePump"] = "SyringePump"
    who_am_i: Literal[1296] = 1296


class HarpNeurophotometricsFP3002(_HarpDeviceBase):
    device_type: Literal["NeurophotometricsFP3002"] = "NeurophotometricsFP3002"
    who_am_i: Literal[2064] = 2064


class HarpIblBehaviorControl(_HarpDeviceBase):
    device_type: Literal["Ibl_behavior_control"] = "Ibl_behavior_control"
    who_am_i: Literal[2080] = 2080


class HarpRfidReader(_HarpDeviceBase):
    device_type: Literal["RfidReader"] = "RfidReader"
    who_am_i: Literal[2094] = 2094


class HarpPluma(_HarpDeviceBase):
    device_type: Literal["Pluma"] = "Pluma"
    who_am_i: Literal[2110] = 2110


class HarpLicketySplit(_HarpDeviceBase):
    device_type: Literal["LicketySplit"] = "LicketySplit"
    who_am_i: Literal[1400] = 1400


class HarpSniffDetector(_HarpDeviceBase):
    device_type: Literal["SniffDetector"] = "SniffDetector"
    who_am_i: Literal[1401] = 1401


class HarpTreadmill(_HarpDeviceBase):
    device_type: Literal["Treadmill"] = "Treadmill"
    who_am_i: Literal[1402] = 1402


class HarpCuttlefish(_HarpDeviceBase):
    device_type: Literal["cuTTLefish"] = "cuTTLefish"
    who_am_i: Literal[1403] = 1403


class HarpWhiteRabbit(_HarpDeviceBase):
    device_type: Literal["WhiteRabbit"] = "WhiteRabbit"
    who_am_i: Literal[1404] = 1404
    connected_clock_outputs: List[ConnectedClockOutput] = Field(default=[], description="Connected clock outputs")

    @field_validator("connected_clock_outputs")
    @classmethod
    def validate_connected_clock_outputs(cls, v: List[ConnectedClockOutput]) -> List[ConnectedClockOutput]:
        return _assert_unique_output_channels(v)


class HarpEnvironmentSensor(_HarpDeviceBase):
    device_type: Literal["EnvironmentSensor"] = "EnvironmentSensor"
    who_am_i: Literal[1405] = 1405


_HarpDevice = Union[
    HarpDeviceGeneric,
    HarpUSBHub,
    HarpPoke,
    HarpMultiPwmGenerator,
    HarpWear,
    HarpWearBaseStationGen2,
    HarpDriver12Volts,
    HarpLedController,
    HarpSynchronizer,
    HarpInputExpander,
    HarpOutputExpander,
    HarpSimpleAnalogGenerator,
    HarpStepperDriver,
    HarpArchimedes,
    HarpOlfactometer,
    HarpClockSynchronizer,
    HarpTimestampGeneratorGen1,
    HarpTimestampGeneratorGen3,
    HarpCameraController,
    HarpCameraControllerGen2,
    HarpPyControlAdapter,
    HarpBehavior,
    HarpVestibularH1,
    HarpVestibularH2,
    HarpLoadCells,
    HarpAnalogInput,
    HarpRgbArray,
    HarpFlyPad,
    HarpSoundCard,
    HarpSyringePump,
    HarpNeurophotometricsFP3002,
    HarpIblBehaviorControl,
    HarpRfidReader,
    HarpPluma,
    HarpLicketySplit,
    HarpSniffDetector,
    HarpTreadmill,
    HarpCuttlefish,
    HarpWhiteRabbit,
    HarpEnvironmentSensor,
]

if TYPE_CHECKING:
    HarpDevice = _HarpDevice
else:
    HarpDevice = TypeAliasType(
        "HarpDevice",
        Annotated[_HarpDevice, Field(discriminator="device_type")],
    )

__all__ = [
    "ConnectedClockOutput",
    "HarpDeviceGeneric",
    "HarpUSBHub",
    "HarpPoke",
    "HarpMultiPwmGenerator",
    "HarpWear",
    "HarpWearBaseStationGen2",
    "HarpDriver12Volts",
    "HarpLedController",
    "HarpSynchronizer",
    "HarpInputExpander",
    "HarpOutputExpander",
    "HarpSimpleAnalogGenerator",
    "HarpStepperDriver",
    "HarpArchimedes",
    "HarpOlfactometer",
    "HarpClockSynchronizer",
    "HarpTimestampGeneratorGen1",
    "HarpTimestampGeneratorGen3",
    "HarpCameraController",
    "HarpCameraControllerGen2",
    "HarpPyControlAdapter",
    "HarpBehavior",
    "HarpVestibularH1",
    "HarpVestibularH2",
    "HarpLoadCells",
    "HarpAnalogInput",
    "HarpRgbArray",
    "HarpFlyPad",
    "HarpSoundCard",
    "HarpSyringePump",
    "HarpNeurophotometricsFP3002",
    "HarpIblBehaviorControl",
    "HarpRfidReader",
    "HarpPluma",
    "HarpLicketySplit",
    "HarpSniffDetector",
    "HarpTreadmill",
    "HarpCuttlefish",
    "HarpWhiteRabbit",
    "HarpEnvironmentSensor",
    "HarpDevice",
]
