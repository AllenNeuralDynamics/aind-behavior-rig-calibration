import unittest
from datetime import datetime

from pydantic import ValidationError

from aind_behavior_services.calibration.water_valve import (
    Measurement,
    WaterValveCalibration,
    WaterValveCalibrationInput,
    WaterValveCalibrationOutput,
)


class WaterValveTests(unittest.TestCase):
    """Tests the water calibration model."""

    def test_calibration(self):
        """Test the compare_version method."""

        _delta_times = [0.1, 0.2, 0.3, 0.4, 0.5]
        _slope = 10.1
        _offset = -0.3
        _water_weights = [water_mock_model(x, _slope, _offset) for x in _delta_times]
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
            date=datetime.now(),
        )

        try:
            WaterValveCalibration.model_validate_json(calibration.model_dump_json())
        except ValidationError as e:
            self.fail(f"Validation failed with error: {e}")

    def test_calibration_on_null_output(self):
        """Test the compare_version method."""

        _delta_times = [0.1, 0.2, 0.3, 0.4, 0.5]
        _slope = 10.1
        _offset = -0.3
        _water_weights = [water_mock_model(x, _slope, _offset) for x in _delta_times]
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
            date=datetime.now(),
        )

        self.assertAlmostEqual(_slope, calibration.output.slope, 2, "Slope is not almost equal")
        self.assertAlmostEqual(_offset, calibration.output.offset, 2, "Offset is not almost equal")
        self.assertAlmostEqual(1.0, calibration.output.r2, 2, "R2 is not almost equal")


def water_mock_model(time: float, slope: float, offset: float) -> float:
    return slope * time + offset


if __name__ == "__main__":
    unittest.main()
