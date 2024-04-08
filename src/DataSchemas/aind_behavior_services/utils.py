import json
import os
import subprocess
from enum import Enum
from os import PathLike
from pathlib import Path
from string import capwords
from subprocess import CompletedProcess, run
from typing import Dict, List, Optional, TypeVar

from pydantic import BaseModel, PydanticInvalidForJsonSchema
from pydantic.json_schema import GenerateJsonSchema, JsonSchemaMode, JsonSchemaValue, _deduplicate_schemas
from pydantic_core import PydanticOmit, core_schema, to_jsonable_python


class CustomGenerateJsonSchema(GenerateJsonSchema):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nullable_as_oneof = kwargs.get("nullable_as_oneof", True)
        self.unions_as_oneof = kwargs.get("unions_as_oneof", True)

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
        expected = [v.value if isinstance(v, Enum) else v for v in schema["expected"]]
        # jsonify the expected values
        expected = [to_jsonable_python(v) for v in expected]

        types = {type(e) for e in expected}

        if len(expected) == 1:
            if isinstance(expected[0], str):
                return {"const": expected[0], "type": "string"}
            elif isinstance(expected[0], int):
                return {"const": expected[0], "type": "integer"}
            elif isinstance(expected[0], float):
                return {"const": expected[0], "type": "number"}
            elif isinstance(expected[0], bool):
                return {"const": expected[0], "type": "boolean"}
            elif isinstance(expected[0], list):
                return {"const": expected[0], "type": "array"}
            elif expected[0] is None:
                return {"const": expected[0], "type": "null"}
            else:
                return {"const": expected[0]}

        if types == {str}:
            return {"enum": expected, "type": "string"}
        elif types == {int}:
            return {"enum": expected, "type": "integer"}
        elif types == {float}:
            return {"enum": expected, "type": "number"}
        elif types == {bool}:
            return {"enum": expected, "type": "boolean"}
        elif types == {list}:
            return {"enum": expected, "type": "array"}
        # there is not None case because if it's mixed it hits the final `else`
        # if it's a single Literal[None] then it becomes a `const` schema above
        else:
            return {"enum": expected}

    def union_schema(self, schema: core_schema.UnionSchema) -> JsonSchemaValue:
        """Generates a JSON schema that matches a schema that allows values matching any of the given schemas.

        Args:
            schema: The core schema.

        Returns:
            The generated JSON schema.
        """
        generated: list[JsonSchemaValue] = []

        choices = schema["choices"]
        for choice in choices:
            # choice will be a tuple if an explicit label was provided
            choice_schema = choice[0] if isinstance(choice, tuple) else choice
            try:
                generated.append(self.generate_inner(choice_schema))
            except PydanticOmit:
                continue
            except PydanticInvalidForJsonSchema as exc:
                self.emit_warning("skipped-choice", exc.message)
        if len(generated) == 1:
            return generated[0]
        if self.unions_as_oneof is True:
            return self.get_flattened_oneof(generated)
        else:
            return self.get_flattened_anyof(generated)


Model = TypeVar("Model", bound=BaseModel)


def export_schema(
    model: Model,
    schema_generator: GenerateJsonSchema = CustomGenerateJsonSchema,
    mode: JsonSchemaMode = "serialization",
    def_keyword: str = "definitions",
):
    """Export the schema of a model to a json file"""
    _model = model.model_json_schema(schema_generator=schema_generator, mode=mode)
    json_model = json.dumps(_model, indent=2)
    json_model = json_model.replace("$defs", def_keyword)
    return json_model


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
        serializer = [BonsaiSgenSerializers.JSON]

    cmd_string = f'bonsai.sgen --schema "{schema_path}" --output "{output_path}"'
    cmd_string += "" if namespace is None else f" --namespace {namespace}"
    cmd_string += "" if root_element is None else f" --root {root_element}"

    if len(serializer) == 0 or BonsaiSgenSerializers.NONE in serializer:
        cmd_string += " --serializer none"
    else:
        cmd_string += " --serializer"
        cmd_string += " ".join([f" {sr.value}" for sr in serializer])

    return run(cmd_string, shell=True, check=True)


def convert_pydantic_to_bonsai(
    models: Dict[str, BaseModel],
    namespace: str = "DataSchema",
    schema_path: PathLike = Path("./src/DataSchemas/"),
    output_path: PathLike = Path("./src/Extensions/"),
    serializer: Optional[List[BonsaiSgenSerializers]] = None,
) -> None:

    for output_model_name, model in models.items():
        with open(os.path.join(schema_path, f"{output_model_name}.json"), "w", encoding="utf-8") as f:
            json_model = export_schema(model)
            f.write(json_model)
        cmd_return = bonsai_sgen(
            schema_path=Path(os.path.join(schema_path, f"{output_model_name}.json")),
            output_path=Path(os.path.join(output_path, f"{snake_to_pascal_case(output_model_name)}.cs")),
            namespace=namespace,
            serializer=serializer,
        )
        print(cmd_return.stdout)


def snake_to_pascal_case(s: str) -> str:
    """
    Converts a snake_case string to PascalCase.

    Args:
        s (str): The snake_case string to be converted.

    Returns:
        str: The PascalCase string.
    """
    return "".join(map(capwords, s.split("_")))


def _build_bonsai_process_command(
    workflow_file: PathLike | str,
    bonsai_exe: PathLike | str = "bonsai/bonsai.exe",
    is_editor_mode: bool = True,
    is_start_flag: bool = True,
    layout: Optional[PathLike | str] = None,
    additional_properties: Optional[Dict[str, str]] = None,
) -> str:

    output_cmd: str = f'"{bonsai_exe}" "{workflow_file}"'
    if is_editor_mode:
        if is_start_flag:
            output_cmd += " --start"
    else:
        output_cmd += " --no-editor"
        if not (layout is None):
            output_cmd += f' --visualizer-layout:"{layout}"'

    if additional_properties:
        for param, value in additional_properties.items():
            output_cmd += f' -p:"{param}"="{value}"'

    return output_cmd


def run_bonsai_process(
    workflow_file: PathLike | str,
    bonsai_exe: PathLike | str = "bonsai/bonsai.exe",
    is_editor_mode: bool = True,
    is_start_flag: bool = True,
    layout: Optional[PathLike | str] = None,
    additional_properties: Optional[Dict[str, str]] = None,
    cwd: Optional[PathLike | str] = None,
    timeout: Optional[float] = None,
    print_cmd: bool = False,
) -> CompletedProcess:

    output_cmd = _build_bonsai_process_command(
        workflow_file=workflow_file,
        bonsai_exe=bonsai_exe,
        is_editor_mode=is_editor_mode,
        is_start_flag=is_start_flag,
        layout=layout,
        additional_properties=additional_properties,
    )
    if cwd is None:
        cwd = os.getcwd()
    if print_cmd:
        print(output_cmd)
    return subprocess.run(output_cmd, cwd=cwd, check=True, timeout=timeout)


def open_bonsai_process(
    workflow_file: PathLike | str,
    bonsai_exe: PathLike | str = "bonsai/bonsai.exe",
    is_editor_mode: bool = True,
    is_start_flag: bool = True,
    layout: Optional[PathLike | str] = None,
    additional_properties: Optional[Dict[str, str]] = None,
    log_file_name: Optional[str] = None,
    cwd: Optional[PathLike | str] = None,
    creation_flags: Optional[int] = None,
    print_cmd: bool = False,
) -> subprocess.Popen:

    output_cmd = _build_bonsai_process_command(
        workflow_file=workflow_file,
        bonsai_exe=bonsai_exe,
        is_editor_mode=is_editor_mode,
        is_start_flag=is_start_flag,
        layout=layout,
        additional_properties=additional_properties,
    )

    if cwd is None:
        cwd = os.getcwd()
    if creation_flags is None:
        creation_flags = subprocess.CREATE_NEW_CONSOLE

    if log_file_name is None:
        if print_cmd:
            print(output_cmd)
        return subprocess.Popen(output_cmd, cwd=cwd, creationflags=creation_flags)
    else:
        logging_cmd = f'powershell -ep Bypass -c "& {output_cmd} *>&1 | tee -a {log_file_name}"'
        if print_cmd:
            print(logging_cmd)
        return subprocess.Popen(logging_cmd, cwd=cwd, creationflags=creation_flags)
