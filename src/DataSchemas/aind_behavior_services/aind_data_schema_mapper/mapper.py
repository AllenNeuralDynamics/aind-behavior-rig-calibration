import os
from pathlib import Path
from typing import Type, TypeVar, Union

from aind_data_schema.core.session import Session, Stream, Modality, StimulusEpoch, Software
from aind_behavior_services import AindBehaviorSessionModel, AindBehaviorRigModel, AindBehaviorTaskLogicModel


TSession = TypeVar("TSession", bound=AindBehaviorSessionModel)
TRig = TypeVar("TRig", bound=AindBehaviorRigModel)
TTaskLogic = TypeVar("TTaskLogic", bound=AindBehaviorTaskLogicModel)
TSchema = TypeVar("TSchema", bound=Union[AindBehaviorSessionModel])

session_root = Path(r"C:\Users\bruno.cruz\OneDrive - Allen Institute\Desktop\Config")
session_path = session_root / "session_input.json"
task_logic_path = session_root / "tasklogic_input.json"
rig_path = session_root / "rig_input.json"


def map_to_aind_data_schema(
    session: TSession,
    rig: TRig,
    task_logic: TTaskLogic,
) -> Session:

    ads_session = Session(
        experimenter_full_name=["NA"],
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
                camera_names=["TBD"],
            )
        ],
        mouse_platform_name="Mouse platform",
        active_mouse_platform=True,
        stimulus_epochs=StimulusEpoch(
            stimulus_start_time=session.date,
            stimulus_end_time=session.date,
            stimulus_modalities=[Modality.BEHAVIOR],
            software=Software(
                name="Bonsai",
                version=session.commit_hash,
                url="https://github.com/AllenNeuralDynamics/Aind.Behavior.VrForaging/blob/{sha}/bonsai/Bonsai.config".format(
                    sha=session.commit_hash
                ),
            ),
            script=Software(
                name="vr-foraging.bonsai",
                version=session.commit_hash,
                url="https://github.com/AllenNeuralDynamics/Aind.Behavior.VrForaging/blob/{sha}/src/vr-foraging.bonsai".format(
                    sha=session.commit_hash
                ),
                parameters=task_logic,
            ),
        ),
    )
    return ads_session


def model_from_json_file(json_path: os.PathLike | str, model_class: Type[TSchema]) -> TSchema:
    with open(json_path, encoding="utf-8") as f:
        return model_class.model_validate_json(f.read())
