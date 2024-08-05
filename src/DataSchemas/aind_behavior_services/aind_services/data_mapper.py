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
from aind_data_schema.core.session import Modality, Session, Software, StimulusEpoch, StimulusModality, Stream

import aind_behavior_services.rig as AbsRig
from aind_behavior_services import (
    AindBehaviorRigModel,
    AindBehaviorSessionModel,
    AindBehaviorTaskLogicModel,
)
from aind_behavior_services.calibration import Calibration

from . import helpers

TSchema = TypeVar("TSchema", bound=Union[AindBehaviorSessionModel, AindBehaviorRigModel, AindBehaviorTaskLogicModel])


def mapper(
    session_data_root: os.PathLike,
    session_model: Type[AindBehaviorSessionModel],
    rig_model: Type[AindBehaviorRigModel],
    task_logic_model: Type[AindBehaviorTaskLogicModel],
    repository: Union[os.PathLike, git.Repo],
    script_path: os.PathLike,
    /,
    session_end_time: datetime.datetime = datetime.datetime.now(),
    **kwargs,
) -> Session:
    session_data_root = Path(session_data_root)
    session = model_from_json_file(session_data_root / "Config" / "session_input.json", session_model)
    rig = model_from_json_file(session_data_root / "Config" / "rig_input.json", rig_model)
    task_logic = model_from_json_file(session_data_root / "Config" / "tasklogic_input.json", task_logic_model)

    # Normalize repository
    if isinstance(repository, os.PathLike):
        repository = git.Repo(Path(repository))
    repository_remote_url = repository.remote().url
    repository_sha = repository.head.commit.hexsha
    repository_relative_script_path = Path(script_path).resolve().relative_to(repository.working_dir)

    # Populate calibrations:
    calibrations = helpers.get_fields_of_type(rig, Calibration)
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

    ##
    aind_data_schema_session = Session(
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
        calibrations=[keyed[1] for keyed in calibrations],
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
                        parameters=helpers.snapshot_bonsai_environment(),  # todo : Consider passing an explicit path here
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


def model_from_json_file(json_path: os.PathLike | str, model_class: Type[TSchema]) -> TSchema:
    with open(json_path, encoding="utf-8") as f:
        return model_class.model_validate_json(f.read())


def model_to_json_file(json_path: os.PathLike | str, model: TSchema) -> None:
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(model.model_dump_json(indent=4))
