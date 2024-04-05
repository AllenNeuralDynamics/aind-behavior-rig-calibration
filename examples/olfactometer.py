import datetime

from aind_behavior_services.session import AindBehaviorSessionModel
from aind_behavior_services.base import get_commit_hash

from aind_behavior_services.calibration.olfactometer import (
    OlfactometerChannelType,
    OlfactometerChannel,
    OlfactometerChannelConfig,
    OlfactometerCalibrationLogic,
    OlfactometerCalibration, OlfactometerCalibrationInput, OlfactometerCalibrationOutput
)


channels_config = [
    OlfactometerChannelConfig(
        channel_index=OlfactometerChannel.Channel0,
        channel_type=OlfactometerChannelType.ODOR,
        flow_rate=100,
        odorant="Banana",
        odorant_dilution=0.1,
    ),
    OlfactometerChannelConfig(
        channel_index=OlfactometerChannel.Channel1,
        channel_type=OlfactometerChannelType.ODOR,
        flow_rate=100,
        odorant="Strawberry",
        odorant_dilution=0.1,
    ),
    OlfactometerChannelConfig(
        channel_index=OlfactometerChannel.Channel2,
        channel_type=OlfactometerChannelType.ODOR,
        flow_rate=100,
        odorant="Apple",
        odorant_dilution=0.1,
    ),
    OlfactometerChannelConfig(
        channel_index=OlfactometerChannel.Channel3, channel_type=OlfactometerChannelType.CARRIER, odorant="Air"
    ),
]

channels_config = {channel.channel_index: channel for channel in channels_config}

calibration = OlfactometerCalibration(input=OlfactometerCalibrationInput(), output=OlfactometerCalibrationOutput())

calibration_logic = OlfactometerCalibrationLogic(
    channel_config=channels_config,
    full_flow_rate=1000,
    n_repeats_per_stimulus=10,
    time_on=1,
    time_off=1,
)

calibration_session = AindBehaviorSessionModel(
    root_path="C:\\Data",
    remote_path=None,
    date=datetime.datetime.now(),
    allow_dirty_repo=False,
    experiment="OlfactometerCalibration",
    experiment_version="0.0.0",
    subject="Olfactometer",
    commit_hash=get_commit_hash(),
)

seed_path = "local/olfactometer_{suffix}.json"
with open(seed_path.format(suffix="calibration_logic"), "w") as f:
    f.write(calibration_logic.model_dump_json(indent=3))
with open(seed_path.format(suffix="session"), "w") as f:
    f.write(calibration_session.model_dump_json(indent=3))
