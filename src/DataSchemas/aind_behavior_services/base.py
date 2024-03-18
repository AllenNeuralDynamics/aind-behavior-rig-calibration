from __future__ import annotations

import warnings
from typing import Any, Callable, get_args

from pydantic import BaseModel, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from semver import Version


class SemVerAnnotation:
    """A class representing semantic version annotations."""

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


def coerce_schema_version(cls: BaseModel, v: str) -> str:
    _default_schema_version = Version.parse(get_args(cls.model_fields["schema_version"].annotation)[0])
    v = Version.parse(v)
    if v > _default_schema_version:
        raise ValueError(
            f"Deserialized schema version ({v}) is greater than the current version({_default_schema_version})."
        )
    elif v < _default_schema_version:
        warnings.warn(
            f"Deserialized schema version ({v}) is less than the current version({_default_schema_version}). Will attempt to coerce the conversion."
        )
        return str(_default_schema_version)
    else:
        return str(v)
