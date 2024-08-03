try:
    import aind_data_schema  # noqa: F401
except ImportError as e:
    e.add_note(
        "The 'aind-data-schema' package is required to use this module. \
            Install the optional dependencies defined in `project.toml' \
                by running `pip install .[aind-services]`"
    )
    raise

import json
import os
import datetime
import git
from pathlib import Path
from typing import Type, TypeVar, Union, get_args

from aind_data_schema.core.session import Modality, Session, Software, StimulusEpoch, Stream, StimulusModality

from aind_behavior_services import (
    AindBehaviorRigModel,
    AindBehaviorSessionModel,
    AindBehaviorTaskLogicModel,
)

from aind_behavior_services.rig import CameraController, CameraTypes

TSchema = TypeVar("TSchema", bound=Union[AindBehaviorSessionModel, AindBehaviorRigModel, AindBehaviorTaskLogicModel])


def mapper(
    session_root: os.PathLike,
    session_model: Type[AindBehaviorSessionModel],
    rig_model: Type[AindBehaviorRigModel],
    task_logic_model: Type[AindBehaviorTaskLogicModel],
    /,
    session_end_time: datetime.datetime = datetime.datetime.now(),
    **kwargs,
) -> Session:
    session_root = Path(session_root)
    session = model_from_json_file(session_root / "Config" / "session_input.json", session_model)
    rig = model_from_json_file(session_root / "Config" / "rig_input.json", rig_model)
    task_logic = model_from_json_file(session_root / "Config" / "tasklogic_input.json", task_logic_model)

    ##
    cameras = get_cameras(rig)

    ## Populate modalities
    modalities = [Modality.BEHAVIOR]
    if any([camera.video_writer for camera in cameras]):
        modalities.append(Modality.BEHAVIOR_VIDEOS)

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
                stream_modalities=[Modality.BEHAVIOR, Modality.BEHAVIOR_VIDEOS],
                stream_start_time=session.date,
                stream_end_time=session_end_time or session.date,
                camera_names=["NULL"],
            ),
        ],
        mouse_platform_name="Mouse platform",
        active_mouse_platform=True,
        stimulus_epochs=[
            StimulusEpoch(
                stimulus_name="vr-foraging task",
                stimulus_start_time=session.date,
                stimulus_end_time=session_end_time,
                stimulus_modalities=[],
                software=[
                    Software(
                        name="Bonsai",
                        version=session.commit_hash,
                        url="https://github.com/AllenNeuralDynamics/Aind.Behavior.VrForaging/blob/{sha}/bonsai/Bonsai.config".format(
                            sha=session.commit_hash
                        ),
                    )
                ],
                script=Software(
                    name="vr-foraging.bonsai",
                    version=session.commit_hash,
                    url="https://github.com/AllenNeuralDynamics/Aind.Behavior.VrForaging/blob/{sha}/src/vr-foraging.bonsai".format(
                        sha=session.commit_hash
                    ),
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



def get_cameras(rig_instance: AindBehaviorRigModel) -> list[CameraTypes]:
    cameras: list[CameraTypes] = []
    for field in rig_instance.model_fields:
        attr = getattr(rig_instance, field)
        if isinstance(attr, CameraController):
            for _, camera in attr.cameras.items():
                if isinstance(camera, get_args(CameraTypes)):
                    cameras.append(camera)
    return cameras


