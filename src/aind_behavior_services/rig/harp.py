from typing_extensions import deprecated

from aind_behavior_services.utils import get_fields_of_type

from ._base import TRig
from ._harp_gen import *  # noqa
from ._harp_gen import ConnectedClockOutput, HarpLicketySplit, HarpTimestampGeneratorGen3, _HarpDeviceBase


def validate_harp_clock_output(rig: TRig) -> TRig:
    harp_devices = get_fields_of_type(rig, _HarpDeviceBase)
    if len(harp_devices) < 2:
        return rig
    n_clock_targets = len(harp_devices) - 1
    clock_outputs = get_fields_of_type(rig, ConnectedClockOutput)
    if len(clock_outputs) != n_clock_targets:
        raise ValueError(f"Expected {n_clock_targets} clock outputs, got {len(clock_outputs)}")
    return rig


# For backwards compatibility


@deprecated("Use HarpTimestampGeneratorGen3 instead.")
class HarpClockGenerator(HarpTimestampGeneratorGen3):
    pass


@deprecated("Use HarpLicketySplit instead.")
class HarpLickometer(HarpLicketySplit):
    pass
