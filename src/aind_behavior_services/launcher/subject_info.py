import logging
from typing import Any, Optional, Self

from pydantic import BaseModel, Field, NonNegativeFloat, TypeAdapter, ValidationError

from aind_behavior_services.session import AindBehaviorSessionModel

logger = logging.getLogger(__name__)


class SubjectInfo(BaseModel):
    subject: str
    animal_weight_prior: Optional[NonNegativeFloat] = Field(
        default=None, description="Subject weight before the session"
    )
    animal_weight_post: Optional[NonNegativeFloat] = Field(default=None, description="Subject weight after the session")
    reward_consumed_total: Optional[NonNegativeFloat] = Field(
        default=None, description="Reward consumed by the subject. "
    )

    @classmethod
    def from_session(cls, session: AindBehaviorSessionModel, **kwargs) -> Self:
        return cls(subject=session.subject, **kwargs)

    def prompt_field(self, field_name: str, default: Optional[Any] = None, abort_if_set: bool = False) -> Self:
        _field = self.model_fields[field_name]
        _type_adaptor: TypeAdapter = TypeAdapter(_field.annotation)
        value: Optional[Any]
        if abort_if_set:
            if field_name in self.model_fields_set:
                raise ValueError(f"Field {field_name} is already set. Use abort_if_set=True to override instead.")
        while True:
            _in = input(f"Enter {field_name} ({_field.description}): ")
            value = _in if _in != "" else default
            try:
                setattr(self, field_name, _type_adaptor.validate_python(value))
                return self.model_validate(self.model_dump())
            except (ValidationError, ValueError) as e:
                logger.error("Error while validating input : %s. %s", value, e)
                continue
