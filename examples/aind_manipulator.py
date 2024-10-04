import os

from aind_behavior_services.base import get_commit_hash
from aind_behavior_services.calibration import aind_manipulator as m
from aind_behavior_services.session import AindBehaviorSessionModel
from aind_behavior_services.utils import utcnow

calibration_data = m.AindManipulatorCalibration(
    device_name="AindManipulatorCalibration",
    input=m.AindManipulatorCalibrationInput(
        full_step_to_mm=m.ManipulatorPosition(x=0.01, y1=0.01, y2=0.01, z=0.01),
        axis_configuration=[
            m.AxisConfiguration(axis=m.Axis.X),
            m.AxisConfiguration(axis=m.Axis.Y1),
            m.AxisConfiguration(axis=m.Axis.Y2),
            m.AxisConfiguration(axis=m.Axis.Z),
        ],
        homing_order=[m.Axis.Y2, m.Axis.Y1, m.Axis.X, m.Axis.Z],
        initial_position=m.ManipulatorPosition(y1=0, y2=0, x=0, z=10000),
    ),
    output=m.AindManipulatorCalibrationOutput(),
    date=utcnow(),
)

calibration_logic = m.CalibrationLogic(task_parameters=m.CalibrationParameters())


calibration_session = AindBehaviorSessionModel(
    root_path="C:\\Data",
    allow_dirty_repo=False,
    experiment="AindManipulatorCalibration",
    date=utcnow(),
    subject="AindManipulator",
    experiment_version="manipulator_control",
    commit_hash=get_commit_hash(),
)

rig = m.CalibrationRig(
    manipulator=m.AindManipulatorDevice(port_name="COM4", calibration=calibration_data),
    rig_name="AindManipulatorRig",
)

seed_path = "local/aind_manipulator_{suffix}.json"
os.makedirs(os.path.dirname(seed_path), exist_ok=True)
with open(seed_path.format(suffix="calibration_logic"), "w") as f:
    f.write(calibration_logic.model_dump_json(indent=3))
with open(seed_path.format(suffix="session"), "w") as f:
    f.write(calibration_session.model_dump_json(indent=3))
with open(seed_path.format(suffix="rig"), "w") as f:
    f.write(rig.model_dump_json(indent=3))
