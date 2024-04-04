import unittest
from datetime import datetime

from aind_behavior_services.base import get_commit_hash
from aind_behavior_services.calibration.water_valve import (
    Measurement,
    WaterValveCalibration,
    WaterValveCalibrationInput,
    WaterValveCalibrationModel,
    WaterValveCalibrationOutput,
    WaterValveOperationControl,
)
from aind_data_schema.models.devices import Calibration
from pydantic import ValidationError


class WaterValveTests(unittest.TestCase):
    """Tests the water calibration model."""

    def test_calibration(self):
        """Test the compare_version method."""

        _delta_times = [0.1, 0.2, 0.3, 0.4, 0.5]
        _slope = 10.1
        _offset = -0.3
        _linear_model = lambda time: _slope * time + _offset
        _water_weights = [_linear_model(x) for x in _delta_times]
        _inputs = [
            Measurement(valve_open_interval=0.5, valve_open_time=t[0], water_weight=[t[1]], repeat_count=1)
            for t in zip(_delta_times, _water_weights)
        ]

        _outputs = WaterValveCalibrationOutput(
            interval_average={interval: volume for interval, volume in zip(_delta_times, _water_weights)},
            slope=_slope,
            offset=_offset,
            r2=1.0,
            valid_domain=[value for value in _delta_times],
        )

        calibration = WaterValveCalibration(
            input=WaterValveCalibrationInput(measurements=_inputs),
            output=_outputs,
            device_name="WaterValve",
            calibration_date=datetime.now(),
        )

        try:
            WaterValveCalibration.model_validate_json(calibration.model_dump_json())
        except ValidationError as e:
            self.fail(f"Validation failed with error: {e}")

        try:
            Calibration.model_validate_json(calibration.model_dump_json())
        except ValidationError as e:
            self.fail(f"Validation failed with error: {e}")

    def test_calibration_on_null_output(self):
        """Test the compare_version method."""

        _delta_times = [0.1, 0.2, 0.3, 0.4, 0.5]
        _slope = 10.1
        _offset = -0.3
        _linear_model = lambda time: _slope * time + _offset
        _water_weights = [_linear_model(x) for x in _delta_times]
        _inputs = WaterValveCalibrationInput(
            measurements=[
                Measurement(valve_open_interval=0.5, valve_open_time=t[0], water_weight=[t[1]], repeat_count=1)
                for t in zip(_delta_times, _water_weights)
            ]
        )

        calibration = WaterValveCalibration(
            input=_inputs,
            output=_inputs.calibrate_output(),
            device_name="WaterValve",
            calibration_date=datetime.now(),
        )

        self.assertAlmostEqual(_slope, calibration.output.slope, 2, "Slope is not almost equal")
        self.assertAlmostEqual(_offset, calibration.output.offset, 2, "Offset is not almost equal")
        self.assertAlmostEqual(1.0, calibration.output.r2, 2, "R2 is not almost equal")

    def test_model(self):
        """Test model serialization"""

        _delta_times = [0.1, 0.2, 0.3, 0.4, 0.5]
        _slope = 10.1
        _offset = -0.3
        _linear_model = lambda time: _slope * time + _offset
        _water_weights = [_linear_model(x) for x in _delta_times]
        _inputs = [
            Measurement(valve_open_interval=0.5, valve_open_time=t[0], water_weight=[t[1]], repeat_count=1)
            for t in zip(_delta_times, _water_weights)
        ]

        _outputs = WaterValveCalibrationOutput(
            interval_average={interval: volume for interval, volume in zip(_delta_times, _water_weights)},
            slope=_slope,
            offset=_offset,
            r2=1.0,
            valid_domain=[value for value in _delta_times],
        )

        input = WaterValveCalibrationInput(measurements=_inputs)
        calibration = WaterValveCalibration(
            input=input,
            output=input.calibrate_output(),
            device_name="WaterValve",
            calibration_date=datetime.now(),
        )

        out_model = WaterValveCalibrationModel(
            calibration=calibration,
            operation_control=WaterValveOperationControl(valve_open_time=[0.1, 0.2, 0.3]),
            root_path="C:\\Data",
            allow_dirty_repo=False,
            experiment="WaterValveCalibration",
            subject="WaterValve",
            experiment_version="WaterValveCalibration",
            commit_hash=get_commit_hash(),
        )

        with open("local/water_valve.json", "w") as f:
            f.write(out_model.model_dump_json(indent=3))


if __name__ == "__main__":
    unittest.main()
