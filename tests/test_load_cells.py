import unittest
from datetime import datetime

from aind_behavior_services.base import get_commit_hash
from aind_behavior_services.calibration.load_cells import (
    LoadCellCalibration,
    LoadCellsCalibration,
    LoadCellsCalibrationInput,
    LoadCellsCalibrationOutput,
    LoadCellsCalibrationModel,
    LoadCellsOperationControl,
)


class LoadCellsTests(unittest.TestCase):

    def test_model(self):

        lc0 = LoadCellCalibration(measured_offset={0: 0.1, 1: 0.2}, measured_weight=[(0.1, 0.1), (0.2, 0.2)])
        lc1 = LoadCellCalibration(measured_offset={0: 0.1, 1: 0.2}, measured_weight=[(0.1, 0.1), (0.2, 0.2)])

        lc_calibration_input = LoadCellsCalibrationInput(channels={0: lc0, 1: lc1})
        lc_calibration_output = LoadCellsCalibrationOutput(
            offset={0: 0, 1: 0},
            baseline={0: 0, 1: 0},
            weight_lookup={0: (0, 0), 1: (0, 0)},
        )

        lc_calibration = LoadCellsCalibration(
            input=lc_calibration_input,
            output=lc_calibration_output,
            device_name="LoadCells",
            calibration_date=datetime.now(),
        )

        lc_op = LoadCellsOperationControl(channels=[0, 1], offset_buffer_size=10)

        out_model = LoadCellsCalibrationModel(
            calibration=lc_calibration,
            operation_control=lc_op,
            root_path="C:\\Data",
            allow_dirty_repo=False,
            experiment="LoadCellsCalibration",
            subject="LoadCells",
            experiment_version="LoadCellsCalibration",
            commit_hash=get_commit_hash(),
        )

        with open("local/load_cells.json", "w") as f:
            f.write(out_model.model_dump_json(indent=3))


if __name__ == "__main__":
    unittest.main()
