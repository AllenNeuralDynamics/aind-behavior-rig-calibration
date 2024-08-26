from enum import StrEnum
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

from aind_behavior_services.base import SchemaVersionedModel

__version__ = "0.1.1"


class DataType(StrEnum):
    STRING = "string"
    NUMBER = "number"
    BOOLEAL = "boolean"
    OBJECT = "object"
    ARRAY = "array"
    NULL = "null"


class TimestampSource(StrEnum):
    NULL = "null"
    HARP = "harp"
    RENDER = "render"


class SoftwareEvent(BaseModel):
    """
    A software event is a generic event that can be used to track any event that occurs in the software.
    """

    name: str = Field(..., description="The name of the event")
    timestamp: Optional[float] = Field(default=None, description="The timestamp of the event")
    timestamp_source: TimestampSource = Field(default=TimestampSource.NULL, description="The source of the timestamp")
    frame_index: Optional[int] = Field(default=None, ge=0, description="The frame index of the event")
    frame_timestamp: Optional[float] = Field(default=None, description="The timestamp of the frame")
    data: Optional[Any] = Field(default=None, description="The data of the event")
    data_type: DataType = Field(default=DataType.NULL, alias="dataType", description="The data type of the event")
    data_type_hint: Optional[str] = Field(default=None, description="The data type hint of the event")


class RenderSynchState(BaseModel):
    sync_quad_value: Optional[float] = Field(default=None, ge=0, le=1, description="The synchronization quad value")
    frame_index: Optional[int] = Field(default=None, ge=0, description="The frame index of the event")
    frame_timestamp: Optional[float] = Field(default=None, ge=0, description="The timestamp of the frame")


class DataTypes(SchemaVersionedModel):
    version: Literal[__version__] = __version__
    software_event: SoftwareEvent
    render_synch_state: RenderSynchState

    class Config:
        json_schema_extra = {
            "x-abstract": "True",
        }
