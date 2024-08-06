import datetime
import unittest
from typing import Dict, List, Literal, Optional

import pydantic
from aind_behavior_services.aind_services import data_mapper
from aind_behavior_services.rig import AindBehaviorRigModel, CameraController, CameraTypes, SpinnakerCamera
from aind_behavior_services.session import AindBehaviorSessionModel
from aind_behavior_services.task_logic import AindBehaviorTaskLogicModel, TaskParameters


class AindServicesTests(unittest.TestCase):
    def test_session_mapper(self):
        data_mapper.mapper(
            session_model=MockSession(),
            rig_model=MockRig(),
            task_logic_model=MockTaskLogic(),
            session_end_time=datetime.datetime.now(),
            repository="./",
            script_path="./src/unit_test.bonsai",
        )


class MockRig(AindBehaviorRigModel):
    version: Literal["0.0.0"] = "0.0.0"
    rig_name: str = pydantic.Field(default="MockRig", description="Rig name")
    camera_controllers: Optional[CameraController[SpinnakerCamera]] = pydantic.Field(
        default=None, description="Camera controllers"
    )
    camera_controllers_2: CameraController[SpinnakerCamera] = pydantic.Field(
        default=CameraController[SpinnakerCamera](
            frame_rate=120, cameras={"cam0": SpinnakerCamera(serial_number="12")}
        ),
        validate_default=True,
    )
    camera_controllers_3: CameraController[SpinnakerCamera] = pydantic.Field(
        default=CameraController[SpinnakerCamera](
            frame_rate=120,
            cameras={"cam0": SpinnakerCamera(serial_number="12"), "cam1": SpinnakerCamera(serial_number="22")},
        ),
        validate_default=True,
    )
    a: List[CameraTypes] = pydantic.Field(default=[SpinnakerCamera(serial_number="12")])


def MockSession() -> AindBehaviorSessionModel:
    return AindBehaviorSessionModel(
        experiment="MockExperiment",
        root_path="MockRootPath",
        subject="MockSubject",
        experiment_version="0.0.0",
    )


class MockTasLogicParameters(TaskParameters):
    foo: int = 1
    bar: str = "bar"
    baz: List[int] = [1, 2, 3]
    qux: Dict[str, int] = {"a": 1, "b": 2, "c": 3}


class MockTaskLogic(AindBehaviorTaskLogicModel):
    version: Literal["0.0.0"] = "0.0.0"
    task_parameters: MockTasLogicParameters = MockTasLogicParameters()
    name: str = "MockTaskLogic"


if __name__ == "__main__":
    unittest.main()
