import datetime
import os

from aind_behavior_services.base import get_commit_hash
from aind_behavior_services.calibration import load_cells as lc
from aind_behavior_services.session import AindBehaviorSessionModel

lc0 = lc.LoadCellCalibration(measured_offset={0: 0.1, 1: 0.2}, measured_weight=[(0.1, 0.1), (0.2, 0.2)])
lc1 = lc.LoadCellCalibration(measured_offset={0: 0.1, 1: 0.2}, measured_weight=[(0.1, 0.1), (0.2, 0.2)])

lc_calibration_input = lc.LoadCellsCalibrationInput(channels={0: lc0, 1: lc1})
lc_calibration_output = lc.LoadCellsCalibrationOutput(
    offset={0: 0, 1: 0},
    baseline={0: 0, 1: 0},
    weight_lookup={0: (0, 0), 1: (0, 0)},
)

calibration = lc.LoadCellsCalibration(
    input=lc_calibration_input,
    output=lc_calibration_output,
    device_name="LoadCells",
    date=datetime.datetime.now(),
)

calibration_logic = lc.CalibrationLogic(
    task_parameters=lc.CalibrationParameters(channels=[0, 1], offset_buffer_size=10)
)

calibration_session = AindBehaviorSessionModel(
    root_path="C:\\Data",
    remote_path=None,
    allow_dirty_repo=False,
    experiment="LoadCellsCalibration",
    date=datetime.datetime.now(),
    subject="LoadCells",
    experiment_version="load_cells",
    commit_hash=get_commit_hash(),
)

rig = lc.CalibrationRig(
    load_cells=lc.LoadCells(port_name="COM4"),
    rig_name="LoadCellsRig",
)

seed_path = "local/load_cells_{suffix}.json"
os.makedirs(os.path.dirname(seed_path), exist_ok=True)

with open(seed_path.format(suffix="calibration_logic"), "w") as f:
    f.write(calibration_logic.model_dump_json(indent=3))
with open(seed_path.format(suffix="session"), "w") as f:
    f.write(calibration_session.model_dump_json(indent=3))
with open(seed_path.format(suffix="rig"), "w") as f:
    f.write(rig.model_dump_json(indent=3))
