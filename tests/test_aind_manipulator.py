import unittest
from datetime import datetime

from aind_behavior_services.calibration import aind_manipulator as m


class AindManipulatorTests(unittest.TestCase):

    def test_model(self):

        calibration = m.AindManipulatorCalibration(
            input=m.AindManipulatorCalibrationInput(
                full_step_to_mm=m.Vector4(x=0.01, y1=0.01, y2=0.01, z=0.01),
                axis_configuration=[
                    m.AxisConfiguration(axis=m.Axis.X),
                    m.AxisConfiguration(axis=m.Axis.Y1),
                    m.AxisConfiguration(axis=m.Axis.Y2),
                    m.AxisConfiguration(axis=m.Axis.Z),
                ],
                homing_order=[m.Axis.Y2, m.Axis.Y1, m.Axis.X, m.Axis.Z],
                initial_position=m.Vector4(y1=0, y2=0, x=0, z=10000),
            ),
            output=m.AindManipulatorCalibrationOutput(),
            calibration_date=datetime.now(),
        )

        out_model = m.AindManipulatorCalibrationModel(
            calibration=calibration,
            root_path="C:\\Data",
            allow_dirty_repo=False,
            experiment="AindManipulatorSettings",
            subject="AindManipulator",
            experiment_version="manipulator_control"
        )

        out_model.model_dump_json(indent=3)


if __name__ == "__main__":
    unittest.main()
