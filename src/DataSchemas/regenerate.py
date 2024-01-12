import json
from pathlib import Path

from aind_behavior_rig.base.json_schema import export_schema
from aind_behavior_rig.calibration.olfactometer import OlfactometerCalibrationModel
from aind_behavior_rig.calibration.water_valve import WaterValveCalibrationModel

OUTPUT_ROOT = Path("./src/DataSchemas/")


# Water Valve Calibration
with open(OUTPUT_ROOT / "water_valve_calibration.json", "w") as f:
    f.write(json.dumps(export_schema(WaterValveCalibrationModel), indent=2))

A = OlfactometerCalibrationModel

# Olfactometer Calibration
with open(OUTPUT_ROOT / "olfactometer_calibration.json", "w") as f:
    f.write(json.dumps(export_schema(OlfactometerCalibrationModel), indent=2))
