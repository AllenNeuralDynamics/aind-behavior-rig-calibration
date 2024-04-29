import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Type, TypeVar, Union

from aind_behavior_services import AindBehaviorRigModel, AindBehaviorSessionModel, AindBehaviorTaskLogicModel
from aind_data_schema.core.session import Modality, Session, Software, StimulusEpoch, Stream

TSession = TypeVar("TSession", bound=AindBehaviorSessionModel)
TRig = TypeVar("TRig", bound=AindBehaviorRigModel)
TTaskLogic = TypeVar("TTaskLogic", bound=AindBehaviorTaskLogicModel)
TSchema = TypeVar("TSchema", bound=Union[AindBehaviorSessionModel, AindBehaviorRigModel, AindBehaviorTaskLogicModel])


def map_to_aind_data_schema(
    session_root: Path,
    session: Type[TSession] = AindBehaviorSessionModel,
    rig: Type[TRig] = AindBehaviorRigModel,
    task_logic: Optional[type[TTaskLogic]] = None,
) -> Session:
    """
    Maps the input session found in `session_root` to the aind-data-schema Session object.

    Args:
        session_root (Path): The root path of the session.
        session (Type[TSession]): The session class.
        rig (Type[TRig]): The rig class.
        task_logic (Type[TTaskLogic]): The task logic class.

    Returns:
        Session: The mapped aind-data-schema session object.
    """

    session_path = session_root / "Config" / "session_input.json"
    task_logic_path = session_root / "Config" / "tasklogic_input.json"
    rig_path = session_root / "Config" / "rig_input.json"

    if task_logic is None:
        return mapper(
            model_from_json_file(session_path, session),
            model_from_json_file(rig_path, rig),
            json.loads((task_logic_path.read_text())),
        )
    else:
        return mapper(
            model_from_json_file(session_path, session),
            model_from_json_file(rig_path, rig),
            model_from_json_file(task_logic_path, task_logic),
        )


def mapper(
    session: TSession,
    rig: TRig,
    task_logic: TTaskLogic | Dict[str, Any],
) -> Session:
    """
    Maps the input session, rig, and task logic to an aind-data-schema Session object.

    Args:
        session (TSession): The input session object.
        rig (TRig): The input rig object.
        task_logic (TTaskLogic): The input task logic object.

    Returns:
        Session: The mapped aind-data-schema Session object.
    """

    if isinstance(task_logic, dict):
        pass
    elif isinstance(task_logic, AindBehaviorTaskLogicModel):
        task_logic = task_logic.model_dump()
    else:
        raise ValueError("task_logic must be a dict or AindBehaviorTaskLogicModel")

    ads_session = Session(
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
                stream_end_time=session.date,
                camera_names=["NULL"],
            ),
        ],
        mouse_platform_name="Mouse platform",
        active_mouse_platform=True,
        stimulus_epochs=[
            StimulusEpoch(
                stimulus_name="vr-foraging task",
                stimulus_start_time=session.date,
                stimulus_end_time=session.date,
                stimulus_modalities=["None"],
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
                    parameters=task_logic,
                ),
            )
        ],
    )
    return ads_session


def model_from_json_file(json_path: os.PathLike | str, model_class: Type[TSchema]) -> TSchema:
    with open(json_path, encoding="utf-8") as f:
        return model_class.model_validate_json(f.read())


def model_to_json_file(json_path: os.PathLike | str, model: TSchema) -> None:
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(model.model_dump_json(indent=4))
