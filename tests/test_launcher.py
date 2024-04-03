import unittest
from aind_behavior_services.launcher import Launcher
from typing import Literal
from pydantic import Field
from aind_behavior_services import AindBehaviorRigModel, AindBehaviorSessionModel, AindBehaviorTaskLogicModel


class LauncherTests(unittest.TestCase):

    def test_instance(self):

        __version__ = "0.1.0"

        class AindGenericTaskRig(AindBehaviorRigModel):
            describedBy: Literal[""] = Field("")
            schema_version: Literal[__version__] = __version__

        class AindGenericTaskSession(AindBehaviorSessionModel):
            describedBy: Literal[""] = Field("")
            schema_version: Literal[__version__] = __version__

        class AindGenericTaskTaskLogic(AindBehaviorTaskLogicModel):
            describedBy: Literal[""] = Field("")
            schema_version: Literal[__version__] = __version__

        launcher = Launcher(
            rig_schema=AindGenericTaskRig,
            session_schema=AindGenericTaskSession,
            task_logic_schema=AindGenericTaskTaskLogic)

        with self.assertRaises((FileNotFoundError, OSError)) as context:
            launcher._validate_dependencies()
            self.assertTrue('This is broken' in context.exception)


if __name__ == "__main__":
    unittest.main()
