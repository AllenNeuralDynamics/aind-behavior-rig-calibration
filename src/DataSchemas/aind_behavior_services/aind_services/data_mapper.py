try:
    import aind_data_schema  # noqa: F401
except ImportError as e:
    e.add_note(
        "The 'aind-data-schema' package is required to use this module. \
            Install the optional dependencies defined in `project.toml' \
                by running `pip install .[aind-services]`"
    )
    raise

import datetime
import os
from pathlib import Path
from typing import Type, TypeVar, Union

import git
from aind_data_schema.core.session import Modality, Session, Software, StimulusEpoch, StimulusModality, Stream, RewardDeliveryConfig, RewardSolution, RewardSpoutConfig, SpoutSide
from aind_data_schema.components.coordinates import RelativePosition
import aind_data_schema.components.devices as ads_devices

import aind_behavior_services.rig as AbsRig
from aind_behavior_services import (
    AindBehaviorRigModel,
    AindBehaviorSessionModel,
    AindBehaviorTaskLogicModel,
)
from aind_behavior_services.calibration import Calibration
from aind_behavior_services.calibration.aind_manipulator import AindManipulatorCalibrationInput



from . import helpers

TSchema = TypeVar("TSchema", bound=Union[AindBehaviorSessionModel, AindBehaviorRigModel, AindBehaviorTaskLogicModel])


def mapper(
    session_data_root: os.PathLike,
    session_model: Type[AindBehaviorSessionModel],
    rig_model: Type[AindBehaviorRigModel],
    task_logic_model: Type[AindBehaviorTaskLogicModel],
    repository: Union[os.PathLike, git.Repo],
    script_path: os.PathLike,
    session_end_time: datetime.datetime = datetime.datetime.now(),
    **kwargs,
) -> Session:
    session_data_root = Path(session_data_root)
    _schema_root = session_data_root / "other" / "Config"
    session = model_from_json_file(_schema_root / "session_input.json", session_model)
    rig = model_from_json_file(_schema_root / "rig_input.json", rig_model)
    print(_schema_root / "tasklogic_input.json")
    task_logic = model_from_json_file(_schema_root / "tasklogic_input.json", task_logic_model)

    # Normalize repository
    if isinstance(repository, os.PathLike | str):
        repository = git.Repo(Path(repository))
    repository_remote_url = repository.remote().url
    repository_sha = repository.head.commit.hexsha
    repository_relative_script_path = Path(script_path).resolve().relative_to(repository.working_dir)

    # Populate calibrations:
    calibrations = [_mapper_calibration(_calibration_model[1], datetime.datetime.now()) for _calibration_model in helpers.get_fields_of_type(rig, Calibration)]
    # Populate cameras
    cameras = helpers.get_cameras(rig, exclude_without_video_writer=True)
    # Populate modalities
    modalities: list[Modality] = [Modality.BEHAVIOR]
    if len(cameras) > 0:
        modalities.append(Modality.BEHAVIOR_VIDEOS)
    modalities = list(set(modalities))
    # Populate stimulus modalities
    stimulus_modalities: list[StimulusModality] = []

    if helpers.get_fields_of_type(rig, AbsRig.Screen):
        stimulus_modalities.extend([StimulusModality.VISUAL, StimulusModality.VIRTUAL_REALITY])
    if helpers.get_fields_of_type(rig, AbsRig.HarpOlfactometer):
        stimulus_modalities.append(StimulusModality.OLFACTORY)
    if helpers.get_fields_of_type(rig, AbsRig.HarpTreadmill):
        stimulus_modalities.append(StimulusModality.WHEEL_FRICTION)

    # Mouse platform

    mouse_platform: str
    if helpers.get_fields_of_type(rig, AbsRig.HarpTreadmill):
        mouse_platform = "Treadmill"
        active_mouse_platform = True
    elif helpers.get_fields_of_type(rig, AbsRig.HarpLoadCells):
        mouse_platform = "TubeWithLoadCells"
        active_mouse_platform = True
    else:
        mouse_platform = "None"
        active_mouse_platform = False

    # Reward delivery
    reward_delivery_config = RewardDeliveryConfig(
        reward_solution=RewardSolution.WATER,
        reward_spouts=[])


    # Construct aind-data-schema session
    aind_data_schema_session = Session(
        animal_weight_post=None,  # todo: fetch/push to slims
        animal_weight_prior=None,  # todo: fetch/push to slims
        reward_consumed_total=None,  # todo: fetch/push to slims
        reward_delivery=reward_delivery_config,
        experimenter_full_name=session.experimenter,
        session_start_time=session.date,
        session_type=session.experiment,
        rig_id=rig.rig_name,
        subject_id=session.subject,
        notes=session.notes,
        data_streams=[
            Stream(
                stream_modalities=modalities,
                stream_start_time=session.date,
                stream_end_time=session_end_time or session.date,
                camera_names=cameras.keys(),
            ),
        ],
        calibrations=calibrations,
        mouse_platform_name=mouse_platform,
        active_mouse_platform=active_mouse_platform,
        stimulus_epochs=[
            StimulusEpoch(
                stimulus_name=session.experiment,
                stimulus_start_time=session.date,
                stimulus_end_time=session_end_time,
                stimulus_modalities=stimulus_modalities,
                software=[
                    Software(
                        name="Bonsai",
                        version=f"{repository_remote_url}/blob/{repository_sha}/bonsai/Bonsai.config",
                        url=f"{repository_remote_url}/blob/{repository_sha}/bonsai",
                        parameters=helpers.snapshot_bonsai_environment(),
                    ),
                    Software(
                        name="Python",
                        version=f"{repository_remote_url}/blob/{repository_sha}/pyproject.toml",
                        url=f"{repository_remote_url}/blob/{repository_sha}",
                        parameters=helpers.snapshot_python_environment(),
                    ),
                ],
                script=Software(
                    name=Path(script_path).stem,
                    version=session.commit_hash,
                    url=f"{repository_remote_url}/blob/{repository_sha}/{repository_relative_script_path}",
                    parameters=task_logic.model_dump(),
                ),
            )
        ],
    )
    return aind_data_schema_session


def model_from_json_file(json_path: os.PathLike, model_class: Type[TSchema]) -> TSchema:
    with open(Path(json_path), encoding="utf-8") as f:
        return model_class.model_validate_json(f.read())


def model_to_json_file(json_path: os.PathLike | str, model: TSchema) -> None:
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(model.model_dump_json(indent=4))


def _mapper_calibration(calibration: Calibration, default_date: datetime.datetime = datetime.datetime.now()) -> ads_devices.Calibration:
    return ads_devices.Calibration(
        device_name=calibration.device_name,
        input=calibration.input.model_dump() if calibration.input else {},
        output=calibration.output.model_dump() if calibration.output else {},
        calibration_date=calibration.date or default_date,
        description=calibration.description if calibration.description else "",
        notes=calibration.notes,
    )