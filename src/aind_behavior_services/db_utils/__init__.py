from __future__ import annotations

from typing import Dict, Literal, Optional

from pydantic import BaseModel, Field

from aind_behavior_services.base import SchemaVersionedModel

# Import core types


__version__ = "0.1.0"


class SubjectEntry(BaseModel):
    task_logic_target: str = Field(..., description="Name of the json file containing the task logic")


class SubjectDataBase(SchemaVersionedModel):
    version: Literal[__version__] = __version__
    subjects: Dict[str, Optional[SubjectEntry]] = Field(
        default_factory=dict, description="List of subjects and their task logic targets"
    )

    def add_subject(self, subject: str, subject_entry: Optional[SubjectEntry] = None):
        if subject in self.subjects:
            raise ValueError(f"Subject {subject} already exists in the database. Use set_subject to update it.")
        self.subjects[subject] = subject_entry

    def remove_subject(self, subject: str) -> Optional[SubjectEntry]:
        if subject not in self.subjects:
            raise ValueError(f"Subject {subject} does not exist in the database.")
        return self.subjects.pop(subject, None)

    def get_subject(self, subject: str) -> Optional[SubjectEntry]:
        return self.subjects.get(subject, None)

    def set_subject(self, subject: str, subject_entry: Optional[SubjectEntry] = None):
        self.subjects[subject] = subject_entry
