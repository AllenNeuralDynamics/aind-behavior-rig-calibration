from aind_behavior_services.calibration import treadmill
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
