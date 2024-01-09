from pydantic import Field
from semver import VersionInfo
from aind_data_schema.base import AindModel


class Version(VersionInfo):
    """Version of the model"""

    @classmethod
    def __get_validators__(cls):
        yield cls.parse

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(examples=["1.0.2", "2.15.3-alpha", "21.3.15-beta+12345"])


class CalibrationModel(AindModel):
    """Base class for all aind-behavior-calibration models"""
    version: Version = Field(..., description="Version of the model.")
