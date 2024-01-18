from typing import TypeVar
from enum import Enum

from pydantic import BaseModel
from pydantic.json_schema import GenerateJsonSchema, JsonSchemaValue, JsonSchemaMode, _deduplicate_schemas
from pydantic_core import core_schema, to_jsonable_python


class CustomGenerateJsonSchema(GenerateJsonSchema):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nullable_as_oneof = kwargs.get("nullable_as_oneof", True)

    def nullable_schema(self, schema: core_schema.NullableSchema) -> JsonSchemaValue:
        null_schema = {"type": "null"}
        inner_json_schema = self.generate_inner(schema["schema"])

        if inner_json_schema == null_schema:
            return null_schema
        else:
            if self.nullable_as_oneof:
                return self.get_flattened_oneof([inner_json_schema, null_schema])
            else:
                return super().get_flattened_anyof([inner_json_schema, null_schema])

    def get_flattened_oneof(self, schemas: list[JsonSchemaValue]) -> JsonSchemaValue:
        members = []
        for schema in schemas:
            if len(schema) == 1 and "oneOf" in schema:
                members.extend(schema["oneOf"])
            else:
                members.append(schema)
        members = _deduplicate_schemas(members)
        if len(members) == 1:
            return members[0]
        return {"oneOf": members}

    def literal_schema(self, schema: core_schema.LiteralSchema) -> JsonSchemaValue:
        """Generates a JSON schema that matches a literal value.

        Args:
            schema: The core schema.

        Returns:
            The generated JSON schema.
        """
        expected = [v.value if isinstance(v, Enum) else v for v in schema['expected']]
        # jsonify the expected values
        expected = [to_jsonable_python(v) for v in expected]

        types = {type(e) for e in expected}

        if len(expected) == 1:
            if isinstance(expected[0], str):
                return {'const': expected[0], 'type': 'string'}
            elif isinstance(expected[0], int):
                return {'const': expected[0], 'type': 'integer'}
            elif isinstance(expected[0], float):
                return {'const': expected[0], 'type': 'number'}
            elif isinstance(expected[0], bool):
                return {'const': expected[0], 'type': 'boolean'}
            elif isinstance(expected[0], list):
                return {'const': expected[0], 'type': 'array'}
            elif expected[0] is None:
                return {'const': expected[0], 'type': 'null'}
            else:
                return {'const': expected[0]}

        if types == {str}:
            return {'enum': expected, 'type': 'string'}
        elif types == {int}:
            return {'enum': expected, 'type': 'integer'}
        elif types == {float}:
            return {'enum': expected, 'type': 'number'}
        elif types == {bool}:
            return {'enum': expected, 'type': 'boolean'}
        elif types == {list}:
            return {'enum': expected, 'type': 'array'}
        # there is not None case because if it's mixed it hits the final `else`
        # if it's a single Literal[None] then it becomes a `const` schema above
        else:
            return {'enum': expected}


Model = TypeVar("Model", bound=BaseModel)


def export_schema(model: Model,
                  schema_generator: GenerateJsonSchema = CustomGenerateJsonSchema,
                  mode: JsonSchemaMode = 'serialization'):
    """Export the schema of a model to a json file"""
    return model.model_json_schema(schema_generator=schema_generator, mode=mode)
