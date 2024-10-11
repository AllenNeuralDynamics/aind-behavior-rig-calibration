import os

from aind_behavior_services.base import get_commit_hash
from aind_behavior_services.calibration import treadmill
from aind_behavior_services.session import AindBehaviorSessionModel
from aind_behavior_services.utils import utcnow

treadmill_calibration = treadmill.TreadmillCalibrationOutput(
    wheel_diameter=10,
    pulses_per_revolution=10000,
    invert_direction=False,
    brake_lookup_calibration=[[0, 0], [0.5, 32768], [1, 65535]],
)

calibration = treadmill.TreadmillCalibration(
    device_name="Treadmill",
    input=treadmill.TreadmillCalibrationInput(),
    output=treadmill_calibration,
    date=utcnow(),
)

calibration_logic = treadmill.CalibrationLogic()

calibration_session = AindBehaviorSessionModel(
    root_path="C:\\Data",
    allow_dirty_repo=False,
    experiment="Calibration",
    date=utcnow(),
    subject="00000",
    experiment_version="treadmill",
    commit_hash=get_commit_hash(),
)

rig = treadmill.CalibrationRig(
    treadmill=treadmill.Treadmill(calibration=calibration, port_name="COM4"),
    rig_name="TreadmillCalibrationRig",
)

seed_path = "local/treadmill_{suffix}.json"
os.makedirs(os.path.dirname(seed_path), exist_ok=True)

with open(seed_path.format(suffix="calibration_logic"), "w") as f:
    f.write(calibration_logic.model_dump_json(indent=3))
with open(seed_path.format(suffix="session"), "w") as f:
    f.write(calibration_session.model_dump_json(indent=3))
with open(seed_path.format(suffix="rig"), "w") as f:
    f.write(rig.model_dump_json(indent=3))
