import datetime
import unittest
from pathlib import Path
from typing import Dict, List, Literal, Optional

import pydantic
import yaml

from aind_behavior_services.launcher import data_mapper_service, watchdog_service
from aind_behavior_services.rig import AindBehaviorRigModel, CameraController, CameraTypes, SpinnakerCamera
from aind_behavior_services.session import AindBehaviorSessionModel
from aind_behavior_services.task_logic import AindBehaviorTaskLogicModel, TaskParameters
from aind_behavior_services.utils import utcnow


class AindServicesTests(unittest.TestCase):
    def test_session_mapper(self):
        data_mapper_service.map(
            session_model=MockSession(),
            rig_model=MockRig(),
            task_logic_model=MockTaskLogic(),
            session_end_time=utcnow(),
            repository=Path("./"),
            script_path=Path("./src/unit_test.bonsai"),
        )

    def test_watchdog_manifest(self):
        _watchdog = watchdog_service.WatchdogClient(
            project_name="Cognitive flexibility in patch foraging", schedule_time=datetime.time(hour=20)
        )

        _aind_behavior_session = MockSession()

        _session = data_mapper_service.map(
            session_model=_aind_behavior_session,
            rig_model=MockRig(),
            task_logic_model=MockTaskLogic(),
            session_end_time=utcnow(),
            repository=Path("./"),
            script_path=Path("./src/unit_test.bonsai"),
        )

        _config = _watchdog.create_manifest_config(
            ads_session=_session,
            source=_aind_behavior_session.root_path,
            destination=_aind_behavior_session.remote_path,
            ads_schemas=["schema1", "schema2"],
            project_name=_watchdog.project_name,
            session_name=_aind_behavior_session.session_name,
            validate_project_name=False,
        )

        self.assertEqual(
            _config,
            watchdog_service.ManifestConfig.model_validate_json(_config.model_dump_json()),
            "Manifest config round trip failed",
        )

        round_via_yaml = watchdog_service.ManifestConfig.model_validate(yaml.safe_load(_watchdog._yaml_dump(_config)))
        self.assertEqual(_config, round_via_yaml, "Manifest config round trip failed via yaml")


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
        subject="0000",
        experiment_version="0.0.0",
        remote_path="MockRemotePath",
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
