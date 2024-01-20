from aind_behavior_services.olfactometer import (
    HarpOlfactometerChannel,
    OlfactometerChannel,
    OlfactometerChannelConfig,
    OlfactometerOperationControl,
)
from aind_data_schema.models.devices import ChannelType

channels_config = [
    OlfactometerChannel(
        channel_index=HarpOlfactometerChannel.Channel0, channel_type=ChannelType.ODOR, flow_capacity=100
    ),
    OlfactometerChannel(
        channel_index=HarpOlfactometerChannel.Channel1, channel_type=ChannelType.ODOR, flow_capacity=100
    ),
    OlfactometerChannel(
        channel_index=HarpOlfactometerChannel.Channel2, channel_type=ChannelType.ODOR, flow_capacity=100
    ),
    OlfactometerChannel(
        channel_index=HarpOlfactometerChannel.Channel3, channel_type=ChannelType.CARRIER, flow_capacity=1000
    ),
]
channels_config = {channel.channel_index: channel for channel in channels_config}

stimuli_config = [
    OlfactometerChannelConfig(channel_index=HarpOlfactometerChannel.Channel0, odorant="Banana", odorant_dilution=0.1),
    OlfactometerChannelConfig(channel_index=HarpOlfactometerChannel.Channel1, odorant="Banana", odorant_dilution=0.1),
    OlfactometerChannelConfig(channel_index=HarpOlfactometerChannel.Channel2, odorant="Banana", odorant_dilution=0.1),
]
stimuli_config = {channel.channel_index: channel for channel in stimuli_config}


OpControl = OlfactometerOperationControl(
    channel_config=channels_config,
    stimulus_config=stimuli_config,
    full_flow_rate=1000,
    n_repeats_per_stimulus=10,
    time_on=1,
    time_off=1,
)

with open("olfactometer.json", "w") as f:
    f.write(OpControl.model_dump_json(indent=3))
