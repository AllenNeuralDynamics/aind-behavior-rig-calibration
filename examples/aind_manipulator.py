from aind_behavior_services.calibration import aind_manipulator as m

import datetime


calibration = m.AindManipulatorCalibration(
    input=m.AindManipulatorCalibrationInput(full_step_to_mm=m.Vector4(x=0.01, y1=0.01, y2=0.01, z=0.01)),
    output=m.AindManipulatorCalibrationOutput(),
    calibration_date=datetime.datetime.now(),
)

op_control = m.AindManipulatorOperationControl(
    axis_configuration=[
        m.AxisConfiguration(axis=m.Axis.X),
        m.AxisConfiguration(axis=m.Axis.Y1),
        m.AxisConfiguration(axis=m.Axis.Y2),
        m.AxisConfiguration(axis=m.Axis.Z),
    ],
    homing_order=[m.Axis.Y2, m.Axis.Y1, m.Axis.X, m.Axis.Z],
    initial_position=m.Vector4(y1=0, y2=0, x=0, z=10000),
)


out_model = m.AindManipulatorCalibrationModel(
    operation_control=op_control,
    calibration=calibration,
    rootPath="C:\\Data",
    allowDirty=False,
    experiment="AindManipulatorSettings",
)

with open("local/aind_manipulator.json", "w") as f:
    f.write(out_model.model_dump_json(indent=3))
