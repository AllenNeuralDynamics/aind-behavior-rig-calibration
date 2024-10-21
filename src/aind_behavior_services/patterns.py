from typing import Annotated, List

from pydantic import Field, RootModel

ValuePair = Annotated[List[float], Field(min_length=2, max_length=2)]


class LookUpTable(RootModel):
    root: List[ValuePair] = Field(..., validate_default=True, min_length=2)
