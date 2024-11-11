from __future__ import annotations

import os
from enum import Enum
from typing import Annotated, Dict, Generic, List, Literal, Optional, TypeVar, Union

from pydantic import BaseModel, Field, field_validator
from typing_extensions import TypeAliasType

from aind_behavior_services.base import SchemaVersionedModel


class Device(BaseModel):
    device_type: str = Field(..., description="Device type")
    additional_settings: Optional[BaseModel] = Field(default=None, description="Additional settings")
    calibration: Optional[BaseModel] = Field(default=None, description="Calibration")


class VideoWriterFfmpeg(BaseModel):
    video_writer_type: Literal["FFMPEG"] = Field(default="FFMPEG")
    frame_rate: int = Field(default=30, ge=0, description="Encoding frame rate")
    container_extension: str = Field(default="mp4", description="Container extension")
    output_arguments: str = Field(
        default='-vf "scale=out_color_matrix=bt709:out_range=full" -c:v h264_nvenc -pix_fmt nv12 -color_range full -colorspace bt709 -color_trc linear -tune hq -preset p4 -rc vbr -cq 12 -b:v 0M -metadata author="Allen Institute for Neural Dynamics" -maxrate 700M -bufsize 350M',  # E501
        description="Output arguments",
    )
    input_arguments: str = Field(
        default="-v verbose -colorspace bt709 -color_primaries bt709 -color_range full -color_trc linear",
        description="Input arguments",
    )


class VideoWriterOpenCv(BaseModel):
    video_writer_type: Literal["OPENCV"] = Field(default="OPENCV")
    frame_rate: int = Field(default=30, ge=0, description="Encoding frame rate")
    container_extension: str = Field(default="avi", description="Container extension")
    four_cc: str = Field(default="FMP4", description="Four character code")


VideoWriter = TypeAliasType(
    "VideoWriter", Annotated[Union[VideoWriterFfmpeg, VideoWriterOpenCv], Field(discriminator="video_writer_type")]
)


class WebCamera(Device):
    device_type: Literal["WebCamera"] = Field(default="WebCamera", description="Device type")
    index: int = Field(default=0, ge=0, description="Camera index")
    video_writer: Optional[VideoWriter] = Field(
        default=None, description="Video writer. If not provided, no video will be saved."
    )


class Rect(BaseModel):
    x: int = Field(default=0, ge=0, description="X coordinate of the top-left corner")
    y: int = Field(default=0, ge=0, description="Y coordinate of the top-left corner")
    width: int = Field(default=0, ge=0, description="Width of the rectangle")
    height: int = Field(default=0, ge=0, description="Height of the rectangle")


class SpinnakerCameraAdcBitDepth(int, Enum):
    ADC8BIT = 0
    ADC10BIT = 1
    ADC12BIT = 2


class SpinnakerCamera(Device):
    device_type: Literal["SpinnakerCamera"] = Field(default="SpinnakerCamera", description="Device type")
    serial_number: str = Field(..., description="Camera serial number")
    binning: int = Field(default=1, ge=1, description="Binning")
    color_processing: Literal["Default", "NoColorProcessing"] = Field(default="Default", description="Color processing")
    exposure: int = Field(default=1000, ge=100, description="Exposure time")
    gain: float = Field(default=0, ge=0, description="Gain")
    gamma: Optional[float] = Field(default=None, ge=0, description="Gamma. If None, will disable gamma correction.")
    adc_bit_depth: Optional[SpinnakerCameraAdcBitDepth] = Field(
        default=SpinnakerCameraAdcBitDepth.ADC8BIT, description="ADC bit depth. If None will be left as default."
    )
    region_of_interest: Rect = Field(default=Rect(), description="Region of interest", validate_default=True)
    video_writer: Optional[VideoWriter] = Field(
        default=None, description="Video writer. If not provided, no video will be saved."
    )

    @field_validator("region_of_interest")
    @classmethod
    def validate_roi(cls, v: Rect) -> Rect:
        if v.width == 0 or v.height == 0:
            if any([x != 0 for x in [v.width, v.height, v.x, v.y]]):
                raise ValueError("If width or height is 0, all other values must be 0")
        return v


CameraTypes = Union[WebCamera, SpinnakerCamera]
TCamera = TypeVar("TCamera", bound=CameraTypes)


class CameraController(Device, Generic[TCamera]):
    device_type: Literal["CameraController"] = "CameraController"
    cameras: Dict[str, TCamera] = Field(..., description="Cameras to be instantiated")
    frame_rate: Optional[int] = Field(default=30, ge=0, description="Frame rate of the trigger to all cameras")


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


HarpDevice = TypeAliasType(
    "HarpDevice",
    Annotated[
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
            HarpEnvironmentSensor,
            HarpWhiteRabbit,
        ],
        Field(discriminator="device_type"),
    ],
)


class Vector3(BaseModel):
    x: float = Field(default=0, description="X coordinate of the point")
    y: float = Field(default=0, description="Y coordinate of the point")
    z: float = Field(default=0, description="Z coordinate of the point")


class DisplayIntrinsics(BaseModel):
    frame_width: int = Field(default=1920, ge=0, description="Frame width (px)")
    frame_height: int = Field(default=1080, ge=0, description="Frame height (px)")
    display_width: float = Field(default=20, ge=0, description="Display width (cm)")
    display_height: float = Field(default=15, ge=0, description="Display width (cm)")


class DisplayExtrinsics(BaseModel):
    rotation: Vector3 = Field(
        default=Vector3(x=0.0, y=0.0, z=0.0), description="Rotation vector (radians)", validate_default=True
    )
    translation: Vector3 = Field(
        default=Vector3(x=0.0, y=1.309016, z=-13.27), description="Translation (in cm)", validate_default=True
    )


class DisplayCalibration(BaseModel):
    intrinsics: DisplayIntrinsics = Field(default=DisplayIntrinsics(), description="Intrinsics", validate_default=True)
    extrinsics: DisplayExtrinsics = Field(default=DisplayExtrinsics(), description="Extrinsics", validate_default=True)


class DisplaysCalibration(BaseModel):
    left: DisplayCalibration = Field(
        default=DisplayCalibration(
            extrinsics=DisplayExtrinsics(
                rotation=Vector3(x=0.0, y=1.0472, z=0.0),
                translation=Vector3(x=-16.6917756, y=1.309016, z=-3.575264),
            )
        ),
        description="Left display calibration",
        validate_default=True,
    )
    center: DisplayCalibration = Field(
        default=DisplayCalibration(
            extrinsics=DisplayExtrinsics(
                rotation=Vector3(x=0.0, y=0.0, z=0.0),
                translation=Vector3(x=0.0, y=1.309016, z=-13.27),
            )
        ),
        description="Center display calibration",
        validate_default=True,
    )
    right: DisplayCalibration = Field(
        default=DisplayCalibration(
            extrinsics=DisplayExtrinsics(
                rotation=Vector3(x=0.0, y=-1.0472, z=0.0),
                translation=Vector3(x=16.6917756, y=1.309016, z=-3.575264),
            )
        ),
        description="Right display calibration",
        validate_default=True,
    )


class Screen(Device):
    device_type: Literal["Screen"] = Field(default="Screen", description="Device type")
    display_index: int = Field(default=1, description="Display index")
    target_render_frequency: float = Field(default=60, description="Target render frequency")
    target_update_frequency: float = Field(default=120, description="Target update frequency")
    texture_assets_directory: str = Field(default="Textures", description="Calibration directory")
    calibration: DisplaysCalibration = Field(
        default=DisplaysCalibration(),
        description="Screen calibration",
    )
    brightness: float = Field(default=0, le=1, ge=-1, description="Brightness")
    contrast: float = Field(default=1, le=1, ge=-1, description="Contrast")


class AindBehaviorRigModel(SchemaVersionedModel):
    computer_name: str = Field(default_factory=lambda: os.environ["COMPUTERNAME"], description="Computer name")
    rig_name: str = Field(..., description="Rig name")
