# Import core types
from __future__ import annotations

import os
from enum import Enum

# Import core types
from typing import Annotated, Any, Literal, Optional, Union

from aind_data_schema.base import AindCoreModel, AindModel
from pydantic import Field, RootModel


__version__ = "0.1.1"


class SpinnakerCamera(AindModel):
    serial_number: str = Field(..., description="Camera serial number")
    binning: int = Field(default=1, ge=1, description="Binning")
    color_processing: Literal["Default", "NoColorProcessing"] = Field(default="Default", description="Color processing")
    exposure: int = Field(default=1000, ge=100, description="Exposure time", units="us")
    frame_rate: int = Field(default=30, ge=1, le=350, description="Frame rate", units="Hz")
    gain: float = Field(default=0, ge=0, description="Gain", units="dB")


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
    GENERIC = "generic"


class HarpDeviceBase(AindModel):
    who_am_i: Optional[int] = Field(default=None, le=9999, ge=0, description="Device WhoAmI")
    device_type: HarpDeviceType = Field(default=HarpDeviceType.GENERIC, description="Device type")
    serial_number: Optional[str] = Field(default=None, description="Device serial number")
    port_name: str = Field(..., description="Device port name")
    additional_settings: Optional[Any] = Field(default=None, description="Additional settings")


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
    who_am_i: Literal[1401] = None


class HarpTreadmill(HarpDeviceBase):
    device_type: Literal[HarpDeviceType.TREADMILL] = HarpDeviceType.TREADMILL
    who_am_i: Literal[1402] = 1402


class HarpCuttlefish(HarpDeviceBase):
    device_type: Literal[HarpDeviceType.CUTTLEFISH] = HarpDeviceType.CUTTLEFISH
    who_am_i: Literal[1403] = 1403


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
        ],
        Field(discriminator="device_type"),
    ]


class WebCamera(AindModel):
    index: int = Field(default=0, ge=0, description="Camera index")


class Screen(AindModel):
    display_index: int = Field(default=1, description="Display index")
    target_render_frequency: float = Field(default=60, description="Target render frequency")
    target_update_frequency: float = Field(default=120, description="Target update frequency")
    calibration_directory: str = Field(default="Calibration\\Monitors\\", description="Calibration directory")
    texture_assets_directory: str = Field(default="Textures", description="Calibration directory")


class Treadmill(AindModel):
    wheel_diameter: float = Field(default=15, ge=0, description="Wheel diameter", units="cm")
    pulses_per_revolution: int = Field(default=28800, ge=1, description="Pulses per revolution")
    invert_direction: bool = Field(default=False, description="Invert direction")


class Valve(AindModel):
    calibration_intercept: float = Field(default=0, description="Calibration intercept")
    calibration_slope: float = Field(default=1, description="Calibration slope")


class AindBehaviorRigModel(AindCoreModel):
    computer_name: str = Field(default_factory=lambda: os.environ["COMPUTERNAME"], description="Computer name")
    rig_name: str = Field(..., description="Rig name")
    schema_version: Literal[__version__] = __version__
