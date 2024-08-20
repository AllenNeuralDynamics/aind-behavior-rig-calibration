import unittest
from typing import Literal

from aind_behavior_services import (
    AindBehaviorRigModel,
    AindBehaviorSessionModel,
    AindBehaviorTaskLogicModel,
)
from aind_behavior_services.launcher import Launcher


class LauncherTests(unittest.TestCase):
    def test_instance(self):
        __version__ = "0.1.0"

        class AindGenericTaskRig(AindBehaviorRigModel):
            version: Literal[__version__] = __version__

        class AindGenericTaskSession(AindBehaviorSessionModel):
            version: Literal[__version__] = __version__

        class AindGenericTaskTaskLogic(AindBehaviorTaskLogicModel):
            version: Literal[__version__] = __version__

        launcher = Launcher(
            rig_schema_model=AindGenericTaskRig,
            session_schema_model=AindGenericTaskSession,
            task_logic_schema_model=AindGenericTaskTaskLogic,
            data_dir="data",
            config_library_dir="config",
            bonsai_workflow="workflow.bonsai",
        )

        with self.assertRaises((FileNotFoundError, OSError)) as context:
            launcher._validate_dependencies()
            self.assertTrue("This is broken" in context.exception)


if __name__ == "__main__":
    unittest.main()
