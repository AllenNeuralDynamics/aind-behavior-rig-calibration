import inspect
import logging
from pathlib import Path

from aind_behavior_services import db_utils
from aind_behavior_services.calibration import aind_manipulator
from aind_behavior_services.data_types import DataTypes
from aind_behavior_services.session import AindBehaviorSessionModel
from aind_behavior_services.utils import (
    convert_pydantic_to_bonsai,
    pascal_to_snake_case,
    snake_to_pascal_case,
)

logger = logging.getLogger(__name__)

SCHEMA_ROOT = Path("./src/schemas")
EXTENSIONS_ROOT = Path("./src/Extensions/")
NAMESPACE_PREFIX = "AindBehaviorServices"


def main():
    models = [
        aind_manipulator.CalibrationLogic,
        aind_manipulator.CalibrationRig,
    ]

    for model in models:
        module_name = inspect.getmodule(model).__name__
        module_name = module_name.split(".")[-1]
        schema_name = f"{module_name}_{pascal_to_snake_case(model.__name__)}"
        namespace = f"{NAMESPACE_PREFIX}.{snake_to_pascal_case(schema_name)}"

        convert_pydantic_to_bonsai(
            {schema_name: model}, schema_path=SCHEMA_ROOT, output_path=EXTENSIONS_ROOT, namespace=namespace
        )

    convert_pydantic_to_bonsai(
        {"aind_behavior_session": AindBehaviorSessionModel},
        schema_path=SCHEMA_ROOT,
        output_path=EXTENSIONS_ROOT,
        namespace=f"{NAMESPACE_PREFIX}.AindBehaviorSession",
    )

    convert_pydantic_to_bonsai({"aind_behavior_data_types": DataTypes}, schema_path=SCHEMA_ROOT, skip_sgen=True)
    convert_pydantic_to_bonsai(
        {"aind_behavior_subject_database": db_utils.SubjectDataBase}, schema_path=SCHEMA_ROOT, skip_sgen=True
    )


if __name__ == "__main__":
    main()
