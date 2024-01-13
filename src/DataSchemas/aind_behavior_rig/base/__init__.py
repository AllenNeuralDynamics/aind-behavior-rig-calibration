from __future__ import annotations

from typing import Any, Callable

import pydantic
from aind_data_schema.base import AindCoreModel, AindModel
from aind_data_schema.models.stimulus import Software
from pydantic import Field, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from semver import Version
from datetime import datetime

class SemVerAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        def validate_from_str(value: str) -> Version:
            return Version.parse(value)

        from_str_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_str_schema,
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(Version),
                    from_str_schema,
                ]
            ),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


class RigCalibrationCoreModel(AindCoreModel, extra="ignore"):
    """Base class for all RigCalibrationCoreModel models"""


class RigCalibrationModel(AindModel, extra="ignore"):
    """Base class for all RigCalibrationModel models"""


class OperationControlModel(RigCalibrationModel):
    """Base class for all aind-behavior operation control models"""


class BonsaiWorkflow(Software):
    """Bonsai workflow"""


class RigCalibrationFullModel(RigCalibrationCoreModel):
    """Base class for all RigCalibrationFullModel models"""

    operation_control: OperationControlModel = Field(..., title="Operation control")
    calibration: pydantic.BaseModel = Field(..., title="Calibration")
    date: datetime = Field(..., title="Date")
    notes: str = Field("", title="Notes")
