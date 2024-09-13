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
from typing import Dict, Optional, Type, TypeVar, Union

import aind_data_schema.components.devices as ads_devices
import git
from aind_data_schema.core.session import (
    Modality,
    RewardDeliveryConfig,
    RewardSolution,
    Session,
    Software,
    StimulusEpoch,
    StimulusModality,
    Stream,
)
from pydantic import BaseModel

import aind_behavior_services.rig as AbsRig
from aind_behavior_services import (
    AindBehaviorRigModel,
    AindBehaviorSessionModel,
    AindBehaviorTaskLogicModel,
)
from aind_behavior_services.calibration import Calibration
from aind_behavior_services.utils import utcnow

from . import helpers


def mapper_from_session_root(
    schema_root: os.PathLike,
    session_model: Type[AindBehaviorSessionModel],
    rig_model: Type[AindBehaviorRigModel],
    task_logic_model: Type[AindBehaviorTaskLogicModel],
    repository: Union[os.PathLike, git.Repo],
    script_path: os.PathLike,
    session_end_time: datetime.datetime = utcnow(),
    output_parameters: Optional[Dict] = None,
    **kwargs,
) -> Session:
    return mapper(
        session_model=model_from_json_file(Path(schema_root) / "session_input.json", session_model),
        rig_model=model_from_json_file(Path(schema_root) / "rig_input.json", rig_model),
        task_logic_model=model_from_json_file(Path(schema_root) / "tasklogic_input.json", task_logic_model),
        repository=repository,
        script_path=script_path,
        session_end_time=session_end_time,
        output_parameters=output_parameters,
        **kwargs,
    )


def mapper_from_json_files(
    session_json: os.PathLike,
    rig_json: os.PathLike,
    task_logic_json: os.PathLike,
    session_model: Type[AindBehaviorSessionModel],
    rig_model: Type[AindBehaviorRigModel],
    task_logic_model: Type[AindBehaviorTaskLogicModel],
    repository: Union[os.PathLike, git.Repo],
    script_path: os.PathLike,
    session_end_time: datetime.datetime = utcnow(),
    output_parameters: Optional[Dict] = None,
    **kwargs,
) -> Session:
    return mapper(
        session_model=model_from_json_file(session_json, session_model),
        rig_model=model_from_json_file(rig_json, rig_model),
        task_logic_model=model_from_json_file(task_logic_json, task_logic_model),
        repository=repository,
        script_path=script_path,
        session_end_time=session_end_time,
        output_parameters=output_parameters,
        **kwargs,
    )


def mapper(
    session_model: AindBehaviorSessionModel,
    rig_model: AindBehaviorRigModel,
    task_logic_model: AindBehaviorTaskLogicModel,
    repository: Union[os.PathLike, git.Repo],
    script_path: os.PathLike,
    session_end_time: datetime.datetime = utcnow(),
    output_parameters: Optional[Dict] = None,
    **kwargs,
) -> Session:
    # Normalize repository
    if isinstance(repository, os.PathLike | str):
        repository = git.Repo(Path(repository))
    repository_remote_url = repository.remote().url
    repository_sha = repository.head.commit.hexsha
    repository_relative_script_path = Path(script_path).resolve().relative_to(repository.working_dir)

    # Populate calibrations:
    calibrations = [
        _mapper_calibration(_calibration_model[1], utcnow())
        for _calibration_model in helpers.get_fields_of_type(rig_model, Calibration)
    ]
    # Populate cameras
    cameras = helpers.get_cameras(rig_model, exclude_without_video_writer=True)
    # populate devices
    devices = [device[0] for device in helpers.get_fields_of_type(rig_model, AbsRig.Device) if device[0]]
    # Populate modalities
    modalities: list[Modality] = [getattr(Modality, "BEHAVIOR")]
    if len(cameras) > 0:
        modalities.append(getattr(Modality, "BEHAVIOR_VIDEOS"))
    modalities = list(set(modalities))
    # Populate stimulus modalities
    stimulus_modalities: list[StimulusModality] = []

    if helpers.get_fields_of_type(rig_model, AbsRig.Screen):
        stimulus_modalities.extend([StimulusModality.VISUAL, StimulusModality.VIRTUAL_REALITY])
    if helpers.get_fields_of_type(rig_model, AbsRig.HarpOlfactometer):
        stimulus_modalities.append(StimulusModality.OLFACTORY)
    if helpers.get_fields_of_type(rig_model, AbsRig.HarpTreadmill):
        stimulus_modalities.append(StimulusModality.WHEEL_FRICTION)

    # Mouse platform

    mouse_platform: str
    if helpers.get_fields_of_type(rig_model, AbsRig.HarpTreadmill):
        mouse_platform = "Treadmill"
        active_mouse_platform = True
    elif helpers.get_fields_of_type(rig_model, AbsRig.HarpLoadCells):
        mouse_platform = "TubeWithLoadCells"
        active_mouse_platform = True
    else:
        mouse_platform = "None"
        active_mouse_platform = False

    # Reward delivery
    reward_delivery_config = RewardDeliveryConfig(reward_solution=RewardSolution.WATER, reward_spouts=[])

    # Construct aind-data-schema session
    aind_data_schema_session = Session(
        animal_weight_post=None,  # todo: fetch/push to slims
        animal_weight_prior=None,  # todo: fetch/push to slims
        reward_consumed_total=None,  # todo: fetch/push to slims
        reward_delivery=reward_delivery_config,
        experimenter_full_name=session_model.experimenter,
        session_start_time=session_model.date,
        session_type=session_model.experiment,
        rig_id=rig_model.rig_name,
        subject_id=session_model.subject,
        notes=session_model.notes,
        data_streams=[
            Stream(
                daq_names=devices,
                stream_modalities=modalities,
                stream_start_time=session_model.date,
                stream_end_time=session_end_time if session_end_time else session_model.date,
                camera_names=list(cameras.keys()),
            ),
        ],
        calibrations=calibrations,
        mouse_platform_name=mouse_platform,
        active_mouse_platform=active_mouse_platform,
        stimulus_epochs=[
            StimulusEpoch(
                stimulus_name=session_model.experiment,
                stimulus_start_time=session_model.date,
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
                    version=session_model.commit_hash if session_model.commit_hash else repository_sha,
                    url=f"{repository_remote_url}/blob/{repository_sha}/{repository_relative_script_path}",
                    parameters=task_logic_model.model_dump(),
                ),
                output_parameters=output_parameters if output_parameters else {},
            )  # type: ignore
        ],
    )  # type: ignore
    return aind_data_schema_session


TSchema = TypeVar("TSchema", bound=BaseModel)


def model_from_json_file(json_path: os.PathLike, model_class: Type[TSchema]) -> TSchema:
    with open(Path(json_path), encoding="utf-8") as f:
        return model_class.model_validate_json(f.read())


def _mapper_calibration(
    calibration: Calibration, default_date: datetime.datetime = utcnow()
) -> ads_devices.Calibration:
    return ads_devices.Calibration(
        device_name=calibration.device_name,
        input=calibration.input.model_dump() if calibration.input else {},
        output=calibration.output.model_dump() if calibration.output else {},
        calibration_date=calibration.date if calibration.date else default_date,
        description=calibration.description if calibration.description else "",
        notes=calibration.notes,
    )
