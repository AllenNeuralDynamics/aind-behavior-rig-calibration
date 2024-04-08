from pathlib import Path

from aind_behavior_services.session import AindBehaviorSessionModel
from aind_behavior_services.calibration.load_cells import LoadCellsCalibrationLogic, LoadCellsCalibrationRig
from aind_behavior_services.calibration.olfactometer import OlfactometerCalibrationLogic, OlfactometerCalibrationRig
from aind_behavior_services.calibration.water_valve import WaterValveCalibrationLogic, WaterValveCalibrationRig
from aind_behavior_services.calibration.aind_manipulator import AindManipulatorCalibrationLogic, AindManipulatorCalibrationRig
from aind_behavior_services.utils import convert_pydantic_to_bonsai


SCHEMA_ROOT = Path("./src/DataSchemas/schemas")
EXTENSIONS_ROOT = Path("./src/Extensions/")
NAMESPACE_PREFIX = "AindBehaviorRigCalibration"


def main():
    models = {
        "olfactometer_calibration": OlfactometerCalibrationLogic,
        "water_valve_calibration": WaterValveCalibrationLogic,
        "load_cells_calibration": LoadCellsCalibrationLogic,
        "aind_manipulator_calibration": AindManipulatorCalibrationLogic,
        "olfactometer_calibration_rig": OlfactometerCalibrationRig,
        "water_valve_calibration_rig": WaterValveCalibrationRig,
        "load_cells_calibration_rig": LoadCellsCalibrationRig,
        "aind_manipulator_calibration_rig": AindManipulatorCalibrationRig,
    }
    convert_pydantic_to_bonsai(
        models, schema_path=SCHEMA_ROOT, output_path=EXTENSIONS_ROOT, namespace_prefix=NAMESPACE_PREFIX
    )

    core_models = {"aind_behavior_session": AindBehaviorSessionModel}
    convert_pydantic_to_bonsai(
        core_models, schema_path=SCHEMA_ROOT, output_path=EXTENSIONS_ROOT, namespace_prefix="AindBehaviorServices"
    )


if __name__ == "__main__":
    main()
