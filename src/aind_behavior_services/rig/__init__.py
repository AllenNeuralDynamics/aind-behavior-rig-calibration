from __future__ import annotations

import os
from enum import Enum, IntEnum, auto
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
        default='-vf "scale=out_color_matrix=bt709:out_range=full,format=bgr24,scale=out_range=full" -c:v h264_nvenc -pix_fmt yuv420p -color_range full -colorspace bt709 -color_trc linear -tune hq -preset p4 -rc vbr -cq 12 -b:v 0M -metadata author="Allen Institute for Neural Dynamics" -maxrate 700M -bufsize 350M',  # E501
        description="Output arguments",
    )
    input_arguments: str = Field(
        default="-colorspace bt709 -color_primaries bt709 -color_range full -color_trc linear",
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


class SpinnakerCameraAdcBitDepth(IntEnum):
    ADC8BIT = 0
    ADC10BIT = 1
    ADC12BIT = 2


class SpinnakerCameraPixelFormat(IntEnum):
    MONO8 = 0
    MONO16 = auto()
    RGB8PACKED = auto()
    BAYERGR8 = auto()
    BAYERRG8 = auto()
    BAYERGB8 = auto()
    BAYERBG8 = auto()
    BAYERGR16 = auto()
    BAYERRG16 = auto()
    BAYERGB16 = auto()
    BAYERBG16 = auto()
    MONO12PACKED = auto()
    BAYERGR12PACKED = auto()
    BAYERRG12PACKED = auto()
    BAYERGB12PACKED = auto()
    BAYERBG12PACKED = auto()
    YUV411PACKED = auto()
    YUV422PACKED = auto()
    YUV444PACKED = auto()
    MONO12P = auto()
    BAYERGR12P = auto()
    BAYERRG12P = auto()
    BAYERGB12P = auto()
    BAYERBG12P = auto()
    YCBCR8 = auto()
    YCBCR422_8 = auto()
    YCBCR411_8 = auto()
    BGR8 = auto()
    BGRA8 = auto()
    MONO10PACKED = auto()
    BAYERGR10PACKED = auto()
    BAYERRG10PACKED = auto()
    BAYERGB10PACKED = auto()
    BAYERBG10PACKED = auto()
    MONO10P = auto()
    BAYERGR10P = auto()
    BAYERRG10P = auto()
    BAYERGB10P = auto()
    BAYERBG10P = auto()
    MONO1P = auto()
    MONO2P = auto()
    MONO4P = auto()
    MONO8S = auto()
    MONO10 = auto()
    MONO12 = auto()
    MONO14 = auto()
    MONO16S = auto()
    MONO32F = auto()
    BAYERBG10 = auto()
    BAYERBG12 = auto()
    BAYERGB10 = auto()
    BAYERGB12 = auto()
    BAYERGR10 = auto()
    BAYERGR12 = auto()
    BAYERRG10 = auto()
    BAYERRG12 = auto()
    RGBA8 = auto()
    RGBA10 = auto()
    RGBA10P = auto()
    RGBA12 = auto()
    RGBA12P = auto()
    RGBA14 = auto()
    RGBA16 = auto()
    RGB8 = auto()
    RGB8_PLANAR = auto()
    RGB10 = auto()
    RGB10_PLANAR = auto()
    RGB10P = auto()
    RGB10P32 = auto()
    RGB12 = auto()
    RGB12_PLANAR = auto()
    RGB12P = auto()
    RGB14 = auto()
    RGB16 = auto()
    RGB16S = auto()
    RGB32F = auto()
    RGB16_PLANAR = auto()
    RGB565P = auto()
    BGRA10 = auto()
    BGRA10P = auto()
    BGRA12 = auto()
    BGRA12P = auto()
    BGRA14 = auto()
    BGRA16 = auto()
    RGBA32F = auto()
    BGR10 = auto()
    BGR10P = auto()
    BGR12 = auto()
    BGR12P = auto()
    BGR14 = auto()
    BGR16 = auto()
    BGR565P = auto()
    R8 = auto()
    R10 = auto()
    R12 = auto()
    R16 = auto()
    G8 = auto()
    G10 = auto()
    G12 = auto()
    G16 = auto()
    B8 = auto()
    B10 = auto()
    B12 = auto()
    B16 = auto()
    COORD3D_ABC8 = auto()
    COORD3D_ABC8_PLANAR = auto()
    COORD3D_ABC10P = auto()
    COORD3D_ABC10P_PLANAR = auto()
    COORD3D_ABC12P = auto()
    COORD3D_ABC12P_PLANAR = auto()
    COORD3D_ABC16 = auto()
    COORD3D_ABC16_PLANAR = auto()
    COORD3D_ABC32F = auto()
    COORD3D_ABC32F_PLANAR = auto()
    COORD3D_AC8 = auto()
    COORD3D_AC8_PLANAR = auto()
    COORD3D_AC10P = auto()
    COORD3D_AC10P_PLANAR = auto()
    COORD3D_AC12P = auto()
    COORD3D_AC12P_PLANAR = auto()
    COORD3D_AC16 = auto()
    COORD3D_AC16_PLANAR = auto()
    COORD3D_AC32F = auto()
    COORD3D_AC32F_PLANAR = auto()
    COORD3D_A8 = auto()
    COORD3D_A10P = auto()
    COORD3D_A12P = auto()
    COORD3D_A16 = auto()
    COORD3D_A32F = auto()
    COORD3D_B8 = auto()
    COORD3D_B10P = auto()
    COORD3D_B12P = auto()
    COORD3D_B16 = auto()
    COORD3D_B32F = auto()
    COORD3D_C8 = auto()
    COORD3D_C10P = auto()
    COORD3D_C12P = auto()
    COORD3D_C16 = auto()
    COORD3D_C32F = auto()
    CONFIDENCE1 = auto()
    CONFIDENCE1P = auto()
    CONFIDENCE8 = auto()
    CONFIDENCE16 = auto()
    CONFIDENCE32F = auto()


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
    pixel_format: Optional[SpinnakerCameraPixelFormat] = Field(
        default=SpinnakerCameraPixelFormat.MONO8, description="Pixel format. If None will be left as default."
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
