from __future__ import annotations

import os
from enum import Enum
from typing import Annotated, Literal, Optional, Union

from aind_behavior_services.base import SchemaVersionedModel
from pydantic import BaseModel, Field, RootModel

# Import core types


__version__ = "0.2.0"


class Device(BaseModel):
    device_type: str = Field(..., description="Device type")
    additional_settings: Optional[BaseModel] = Field(default=None, description="Additional settings")
    calibration: Optional[BaseModel] = Field(default=None, description="Calibration")


class SpinnakerCamera(Device):
    device_type: Literal["SpinnakerCamera"] = Field(default="SpinnakerCamera", description="Device type")
    serial_number: str = Field(..., description="Camera serial number")
    binning: int = Field(default=1, ge=1, description="Binning")
    color_processing: Literal["Default", "NoColorProcessing"] = Field(default="Default", description="Color processing")
    exposure: int = Field(default=1000, ge=100, description="Exposure time")
    frame_rate: int = Field(default=30, ge=1, le=350, description="Frame rate")
    gain: float = Field(default=0, ge=0, description="Gain")


class HarpDeviceType(str, Enum):
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
    GENERIC = "generic"


class HarpDeviceBase(BaseModel):
    who_am_i: Optional[int] = Field(default=None, le=9999, ge=0, description="Device WhoAmI")
    device_type: HarpDeviceType = Field(default=HarpDeviceType.GENERIC, description="Device type")
    serial_number: Optional[str] = Field(default=None, description="Device serial number")
    port_name: str = Field(..., description="Device port name")


class HarpBehavior(HarpDeviceBase):
    device_type: Literal[HarpDeviceType.BEHAVIOR] = HarpDeviceType.BEHAVIOR
    who_am_i: Literal[1216] = 1216


class HarpSoundCard(HarpDeviceBase):
    device_type: Literal[HarpDeviceType.SOUNDCARD] = HarpDeviceType.SOUNDCARD
    who_am_i: Literal[1280] = 1280


class HarpLoadCells(HarpDeviceBase):
    device_type: Literal[HarpDeviceType.LOADCELLS] = HarpDeviceType.LOADCELLS
    who_am_i: Literal[1232] = 1232


class HarpOlfactometer(HarpDeviceBase):
    device_type: Literal[HarpDeviceType.OLFACTOMETER] = HarpDeviceType.OLFACTOMETER
    who_am_i: Literal[1140] = 1140


class HarpClockGenerator(HarpDeviceBase):
    device_type: Literal[HarpDeviceType.CLOCKGENERATOR] = HarpDeviceType.CLOCKGENERATOR
    who_am_i: Literal[1158] = 1158


class HarpClockSynchronizer(HarpDeviceBase):
    device_type: Literal[HarpDeviceType.CLOCKSYNCHRONIZER] = HarpDeviceType.CLOCKSYNCHRONIZER
    who_am_i: Literal[1152] = 1152


class HarpAnalogInput(HarpDeviceBase):
    device_type: Literal[HarpDeviceType.ANALOGINPUT] = HarpDeviceType.ANALOGINPUT
    who_am_i: Literal[1236] = 1236


class HarpLickometer(HarpDeviceBase):
    device_type: Literal[HarpDeviceType.LICKOMETER] = HarpDeviceType.LICKOMETER
    who_am_i: Literal[1400] = 1400


class HarpSniffDetector(HarpDeviceBase):
    device_type: Literal[HarpDeviceType.SNIFFDETECTOR] = HarpDeviceType.SNIFFDETECTOR
    who_am_i: Literal[1401] = 1401


class HarpTreadmill(HarpDeviceBase):
    device_type: Literal[HarpDeviceType.TREADMILL] = HarpDeviceType.TREADMILL
    who_am_i: Literal[1402] = 1402


class HarpCuttlefish(HarpDeviceBase):
    device_type: Literal[HarpDeviceType.CUTTLEFISH] = HarpDeviceType.CUTTLEFISH
    who_am_i: Literal[1403] = 1403


class HarpStepperDriver(HarpDeviceBase):
    device_type: Literal[HarpDeviceType.STEPPERDRIVER] = HarpDeviceType.STEPPERDRIVER
    who_am_i: Literal[1130] = 1130


class HarpDevice(RootModel):
    root: Annotated[
        Union[
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
        ],
        Field(discriminator="device_type"),
    ]


class WebCamera(Device):
    device_type: Literal["WebCamera"] = Field(default="WebCamera", description="Device type")
    index: int = Field(default=0, ge=0, description="Camera index")


class Screen(Device):
    device_type: Literal["Screen"] = Field(default="Screen", description="Device type")
    display_index: int = Field(default=1, description="Display index")
    target_render_frequency: float = Field(default=60, description="Target render frequency")
    target_update_frequency: float = Field(default=120, description="Target update frequency")
    calibration_directory: str = Field(default="Calibration\\Monitors\\", description="Calibration directory")
    texture_assets_directory: str = Field(default="Textures", description="Calibration directory")


class Treadmill(BaseModel):
    wheel_diameter: float = Field(default=15, ge=0, description="Wheel diameter")
    pulses_per_revolution: int = Field(default=28800, ge=1, description="Pulses per revolution")
    invert_direction: bool = Field(default=False, description="Invert direction")


class AindBehaviorRigModel(SchemaVersionedModel):
    computer_name: str = Field(default_factory=lambda: os.environ["COMPUTERNAME"], description="Computer name")
    rig_name: str = Field(..., description="Rig name")
    schema_version: Literal[__version__] = __version__
