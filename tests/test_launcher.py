import logging
import unittest
from pathlib import Path
from typing import Literal

from aind_behavior_services import (
    AindBehaviorRigModel,
    AindBehaviorSessionModel,
    AindBehaviorTaskLogicModel,
)
from aind_behavior_services.launcher import Launcher, logging_helper


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
            data_dir=Path("data"),
            config_library_dir=Path("config"),
            bonsai_workflow=Path("workflow.bonsai"),
            logger=dummy_logger(),
        )

        with self.assertRaises((FileNotFoundError, OSError, SystemExit)) as _:
            launcher._validate_dependencies()

    def test_logger(self):
        logger = logging_helper.default_logger_factory(None)
        self.assertIsInstance(logger, logging.Logger)


def dummy_logger() -> logging.Logger:
    logger = logging.getLogger("dummy")
    logger.setLevel(logging.CRITICAL)
    return logger


if __name__ == "__main__":
    unittest.main()
