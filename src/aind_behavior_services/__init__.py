__version__ = "0.8.9"

import logging

from .rig import AindBehaviorRigModel  # noqa: F401
from .session import AindBehaviorSessionModel  # noqa: F401
from .task_logic import AindBehaviorTaskLogicModel  # noqa: F401

logger = logging.getLogger(__name__)
