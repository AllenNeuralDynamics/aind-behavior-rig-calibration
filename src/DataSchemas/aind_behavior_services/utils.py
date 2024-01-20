from enum import Enum
from os import PathLike
from string import capwords
from subprocess import CompletedProcess, run
from typing import List, Optional, TypeVar

from pydantic import BaseModel
from pydantic.json_schema import GenerateJsonSchema, JsonSchemaValue, _deduplicate_schemas
from pydantic_core import core_schema


class CustomGenerateJsonSchema(GenerateJsonSchema):
    """
    A custom class that extends the GenerateJsonSchema class.
    """

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


Model = TypeVar("Model", bound=BaseModel)


def export_schema(model: Model, schema_generator: GenerateJsonSchema = CustomGenerateJsonSchema):
    """Export the schema of a model to a json file"""
    return model.model_json_schema(schema_generator=schema_generator)


class BonsaiSgenSerializers(Enum):
    NONE = "None"
    JSON = "NewtonsoftJson"
    YAML = "YamlDotNet"


def bonsai_sgen(
    schema_path: PathLike,
    output_path: PathLike,
    namespace: str = "DataSchema",
    root_element: Optional[str] = None,
    serializer: Optional[List[BonsaiSgenSerializers]] = None,
) -> CompletedProcess:
    """Runs Bonsai.SGen to generate a Bonsai-compatible schema from a json-schema model
    For more information run `bonsai.sgen --help` in the command line.

    Returns:
        CompletedProcess: The result of running the command.
    Args:
        schema_path (PathLike): Target Json Schema file
        output_path (PathLike): Specifies the name of the file containing the generated code.
        namespace (Optional[str], optional): Specifies the namespace to use for all generated serialization classes. Defaults to DataSchema.
        root_element (Optional[str], optional):  Specifies the name of the class used to represent the schema root element. If None, it will use the json schema root element. Defaults to None.
        serializer (Optional[List[BonsaiSgenSerializers]], optional): Specifies the serializer data annotations to include in the generated classes. Defaults to None.
    """

    if serializer is None:
        serializer = [BonsaiSgenSerializers.JSON, BonsaiSgenSerializers.YAML]

    cmd_string = f'bonsai.sgen --schema "{schema_path}" --output "{output_path}"'
    cmd_string += "" if namespace is None else f" --namespace {namespace}"
    cmd_string += "" if root_element is None else f" --root {root_element}"

    if len(serializer) == 0 or BonsaiSgenSerializers.NONE in serializer:
        cmd_string += " --serializer none"
    else:
        cmd_string += " --serializer"
        cmd_string += " ".join([f" {sr.value}" for sr in serializer])

    return run(cmd_string, shell=True, check=True)


def snake_to_pascal_case(s: str) -> str:
    """
    Converts a snake_case string to PascalCase.

    Args:
        s (str): The snake_case string to be converted.

    Returns:
        str: The PascalCase string.
    """
    return "".join(map(capwords, s.split("_")))
