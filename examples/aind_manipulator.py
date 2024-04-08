import datetime

from aind_behavior_services.base import get_commit_hash
from aind_behavior_services.calibration import aind_manipulator as m
from aind_behavior_services.session import AindBehaviorSessionModel

calibration_data = m.AindManipulatorCalibration(
    name="AindManipulatorCalibration",
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
    calibration_date=datetime.datetime.now(),
)

calibration_logic = m.CalibrationLogic()


calibration_session = AindBehaviorSessionModel(
    root_path="C:\\Data",
    remote_path=None,
    allow_dirty_repo=False,
    experiment="AindManipulatorCalibration",
    date=datetime.datetime.now(),
    subject="AindManipulator",
    experiment_version="manipulator_control",
    commit_hash=get_commit_hash(),
)

seed_path = "local/aind_manipulator_{suffix}.json"
with open(seed_path.format(suffix="calibration_logic"), "w") as f:
    f.write(calibration_logic.model_dump_json(indent=3))
with open(seed_path.format(suffix="session"), "w") as f:
    f.write(calibration_session.model_dump_json(indent=3))
