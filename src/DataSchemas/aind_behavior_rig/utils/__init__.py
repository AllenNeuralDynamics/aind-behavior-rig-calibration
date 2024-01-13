from enum import Enum
from os import PathLike
from subprocess import CompletedProcess, run
from typing import List, Optional
from string import capwords
import pydantic


def build_json_schema(model: pydantic.BaseModel):
    """Build a JSON schema model from a pydantic model"""
    return model.model_json_schema(indent=2)


class BonsaiSgenSerializers(Enum):
    NONE = "None"
    JSON = "NewtonsoftJson"
    YAML = "YamlDotNet"


def bonsai_sgen(
    schema_path: PathLike,
    output_path: PathLike,
    namespace: str = "DataSchema",
    root_element: Optional[str] = None,
    serializer: List[BonsaiSgenSerializers] = [BonsaiSgenSerializers.JSON, BonsaiSgenSerializers.YAML],
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
        serializer (List[BonsaiSgenSerializers], optional): Specifies the serializer data annotations to include in the generated classes. Defaults to [BonsaiSgenSerializers.JSON, BonsaiSgenSerializers.YAML].
    """

    cmd_string = f"bonsai.sgen --schema \"{schema_path}\" --output \"{output_path}\""
    cmd_string += "" if namespace is None else f" --namespace {namespace}"
    cmd_string += "" if root_element is None else f" --root {root_element}"

    if len(serializer) == 0 or BonsaiSgenSerializers.NONE in serializer:
        cmd_string += " --serializer none"
    else:
        cmd_string += " --serializer"
        cmd_string += " ".join([f" {sr.value}" for sr in serializer])

    return run(cmd_string, shell=True, check=True)


def snake_to_pascale_case(s: str) -> str:
    """
    Converts a snake_case string to PascalCase.

    Args:
        s (str): The snake_case string to be converted.

    Returns:
        str: The PascalCase string.
    """
    return "".join(map(capwords, s.split("_")))