import unittest
import warnings
from typing import Literal

from aind_behavior_services import AindBehaviorTaskLogicModel
from aind_behavior_services.task_logic import TaskParameters
from pydantic import Field, ValidationError

version_pre: str = "0.0.1"
version_post: str = "0.0.2"


class AindBehaviorRigModelPre(AindBehaviorTaskLogicModel):
    version: Literal[version_pre] = version_pre
    name: str = Field(default="Pre")
    task_parameters: TaskParameters = Field(default=TaskParameters(), validate_default=True)


class AindBehaviorRigModelPost(AindBehaviorTaskLogicModel):
    version: Literal[version_post] = version_post
    name: str = Field(default="Post")
    task_parameters: TaskParameters = Field(default=TaskParameters(), validate_default=True)


class SchemaVersionCoercionTest(unittest.TestCase):
    def test_version_update_coercion(self):
        pre_instance = AindBehaviorRigModelPre()
        post_instance = AindBehaviorRigModelPost()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                pre_updated = AindBehaviorRigModelPost.model_validate_json(pre_instance.model_dump_json())
            except ValidationError as e:
                self.fail(f"Validation failed with error: {e}")

            self.assertEqual(pre_updated.version, post_instance.version, "Schema version was not coerced correctly.")


if __name__ == "__main__":
    unittest.main()
