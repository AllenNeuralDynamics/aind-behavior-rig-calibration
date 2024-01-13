import json
from pathlib import Path

from aind_behavior_rig.base.json_schema import export_schema
from aind_behavior_rig.olfactometer import OlfactometerCalibrationModel
from aind_behavior_rig.water_valve import WaterValveCalibrationModel
from aind_behavior_rig.utils import bonsai_sgen, BonsaiSgenSerializers

SCHEMA_ROOT = Path("./src/DataSchemas/")
EXTENSIONS_ROOT = Path("./src/Extensions/")



a = BonsaiSgenSerializers.JSON
print(a & BonsaiSgenSerializers.YAML != BonsaiSgenSerializers.NONE)
print(a)

# Water Valve Calibration
with open(SCHEMA_ROOT / "water_valve_calibration.json", "w") as f:
    f.write(json.dumps(export_schema(WaterValveCalibrationModel), indent=2))



# Olfactometer Calibration
with open(SCHEMA_ROOT / "olfactometer_calibration.json", "w") as f:
    f.write(json.dumps(export_schema(OlfactometerCalibrationModel), indent=2))
