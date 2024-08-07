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
            rig_schema=AindGenericTaskRig,
            session_schema=AindGenericTaskSession,
            task_logic_schema=AindGenericTaskTaskLogic,
            data_dir="data",
            config_library_dir="config",
            workflow="workflow.bonsai",
        )

        with self.assertRaises((FileNotFoundError, OSError)) as context:
            launcher._validate_dependencies()
            self.assertTrue("This is broken" in context.exception)


if __name__ == "__main__":
    unittest.main()
