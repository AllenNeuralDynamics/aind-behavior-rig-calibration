from aind_data_schema.base import AindCoreModel
from typing import Literal


__version__ = "0.1.0"


class AindBehaviorTaskLogicModel(AindCoreModel):
    schema_version: Literal[__version__] = Field(default=__version__)
