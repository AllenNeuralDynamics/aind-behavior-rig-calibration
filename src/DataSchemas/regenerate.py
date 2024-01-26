from pathlib import Path
from aind_behavior_services.calibration.olfactometer import OlfactometerCalibrationModel
from aind_behavior_services.calibration.water_valve import WaterValveCalibrationModel
from aind_behavior_services.utils import convert_pydantic_to_bonsai

SCHEMA_ROOT = Path("./src/DataSchemas/")
EXTENSIONS_ROOT = Path("./src/Extensions/")
NAMESPACE_PREFIX = "AindBehaviorRigCalibration"


def main():
    models = {
        "olfactometer_calibration": OlfactometerCalibrationModel,
        "water_valve_calibration": WaterValveCalibrationModel,
    }
    convert_pydantic_to_bonsai(
        models, schema_path=SCHEMA_ROOT, output_path=EXTENSIONS_ROOT, namespace_prefix=NAMESPACE_PREFIX
    )


if __name__ == "__main__":
    main()
