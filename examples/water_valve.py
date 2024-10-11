import os

from aind_behavior_services.base import get_commit_hash
from aind_behavior_services.calibration import water_valve as wv
from aind_behavior_services.session import AindBehaviorSessionModel
from aind_behavior_services.utils import utcnow


def linear_model(time, slope, offset):
    return slope * time + offset


_delta_times = [0.1, 0.2, 0.3, 0.4, 0.5]
_slope = 10.1
_offset = -0.3

_water_weights = [linear_model(x, _slope, _offset) for x in _delta_times]
_inputs = [
    wv.Measurement(valve_open_interval=0.5, valve_open_time=t[0], water_weight=[t[1]], repeat_count=1)
    for t in zip(_delta_times, _water_weights)
]


_outputs = wv.WaterValveCalibrationOutput(
    interval_average={interval: volume for interval, volume in zip(_delta_times, _water_weights)},
    slope=_slope,
    offset=_offset,
    r2=1.0,
    valid_domain=[value for value in _delta_times],
)

input = wv.WaterValveCalibrationInput(measurements=_inputs)

calibration = wv.WaterValveCalibration(
    input=input,
    output=input.calibrate_output(),
    device_name="WaterValve",
    date=utcnow(),
)

calibration_logic = wv.CalibrationLogic(
    task_parameters=wv.CalibrationParameters(valve_open_time=_delta_times, valve_open_interval=0.5, repeat_count=200)
)

calibration_session = AindBehaviorSessionModel(
    root_path="C:\\Data",
    allow_dirty_repo=False,
    experiment="WaterValveCalibration",
    subject="WaterValve",
    experiment_version="WaterValveCalibration",
    commit_hash=get_commit_hash(),
    date=utcnow(),
)

rig = wv.CalibrationRig(rig_name="WaterValveRig")

seed_path = "local/water_valve_{suffix}.json"
os.makedirs(os.path.dirname(seed_path), exist_ok=True)

with open(seed_path.format(suffix="calibration_logic"), "w") as f:
    f.write(calibration_logic.model_dump_json(indent=3))
with open(seed_path.format(suffix="session"), "w") as f:
    f.write(calibration_session.model_dump_json(indent=3))
with open(seed_path.format(suffix="rig"), "w") as f:
    f.write(rig.model_dump_json(indent=3))
