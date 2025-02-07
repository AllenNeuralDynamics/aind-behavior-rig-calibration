from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from ._base import Device


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
