from aind_behavior_services.calibration import load_cells as lc
from aind_behavior_services.utils import utcnow

lc0 = lc.LoadCellCalibrationInput(
    channel=0,
    offset_measurement=[lc.MeasuredOffset(offset=100, baseline=0.1)],
    weight_measurement=[lc.MeasuredWeight(weight=0.1, baseline=0.1)],
)
lc1 = lc.LoadCellCalibrationInput(
    channel=1,
    offset_measurement=[lc.MeasuredOffset(offset=100, baseline=0.1)],
    weight_measurement=[lc.MeasuredWeight(weight=0.1, baseline=0.1)],
)

lc_calibration_input = lc.LoadCellsCalibrationInput(channels=[lc1, lc0])
lc_calibration_output = lc.LoadCellsCalibrationOutput(
    channels=[
        lc.LoadCellCalibrationOutput(channel=0, offset=6, baseline=1000, weight_lookup=[]),
        lc.LoadCellCalibrationOutput(channel=1, offset=6, baseline=1000, weight_lookup=[]),
    ]
)

calibration = lc.LoadCellsCalibration(
    input=lc_calibration_input,
    output=lc_calibration_output,
    device_name="LoadCells",
    date=utcnow(),
)
