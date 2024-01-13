import json
from pathlib import Path
from string import capwords

from aind_behavior_rig.base.json_schema import export_schema
from aind_behavior_rig.olfactometer import OlfactometerCalibrationModel
from aind_behavior_rig.water_valve import WaterValveCalibrationModel
from aind_behavior_rig.utils import bonsai_sgen, BonsaiSgenSerializers, snake_to_pascale_case

SCHEMA_ROOT = Path("./src/DataSchemas/")
EXTENSIONS_ROOT = Path("./src/Extensions/")
NAMESPACE_PREFIX = "AindBehaviorRigCalibration"
SGEN_SERIALIZERS = [BonsaiSgenSerializers.JSON, BonsaiSgenSerializers.YAML]


def main():
    models = {
        'olfactometer_calibration': OlfactometerCalibrationModel,
        'water_valve_calibration': WaterValveCalibrationModel
    }
    for output_model_name, model in models.items():
        with open(SCHEMA_ROOT / f"{output_model_name}.json", "w") as f:
            json_model = json.dumps(export_schema(model), indent=2)
            json_model = json_model.replace("$defs", "definitions")
            f.write(json_model)
        cmd_return = bonsai_sgen(
            schema_path=SCHEMA_ROOT / f"{output_model_name}.json",
            output_path=EXTENSIONS_ROOT / f"{snake_to_pascale_case(output_model_name)}.cs",
            namespace=f"{NAMESPACE_PREFIX}.{snake_to_pascale_case(output_model_name)}",
            serializer=SGEN_SERIALIZERS
            )
        print(cmd_return.stdout)

if __name__ == "__main__":
    main()
