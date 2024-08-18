import unittest
import warnings
from typing import Literal

from aind_behavior_services import AindBehaviorTaskLogicModel
from aind_behavior_services.base import SchemaVersionedModel
from aind_behavior_services.task_logic import TaskParameters
from pydantic import Field, ValidationError

version_pre: str = "0.0.1"
version_post: str = "0.0.2"


class AindBehaviorTaskLogicModelPre(AindBehaviorTaskLogicModel):
    version: Literal[version_pre] = version_pre
    name: str = Field(default="Pre")
    task_parameters: TaskParameters = Field(default=TaskParameters(), validate_default=True)


class AindBehaviorTaskLogicModelPost(AindBehaviorTaskLogicModel):
    version: Literal[version_post] = version_post
    name: str = Field(default="Post")
    task_parameters: TaskParameters = Field(default=TaskParameters(), validate_default=True)


class SchemaVersionedModelPre(SchemaVersionedModel):
    version: Literal[version_post] = version_post
    aind_behavior_services_pkg_version: Literal["0.0.0"] = "0.0.0"


class SchemaVersionedModelPost(SchemaVersionedModel):
    version: Literal[version_post] = version_post


class SchemaVersionCoercionTest(unittest.TestCase):
    def test_version_update_forwards_coercion(self):
        pre_instance = AindBehaviorTaskLogicModelPre()
        post_instance = AindBehaviorTaskLogicModelPost()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                pre_updated = AindBehaviorTaskLogicModelPost.model_validate_json(pre_instance.model_dump_json())
            except ValidationError as e:
                self.fail(f"Validation failed with error: {e}")

            self.assertEqual(pre_updated.version, post_instance.version, "Schema version was not coerced correctly.")

    def test_version_update_backwards_coercion(self):
        post_instance = AindBehaviorTaskLogicModelPost()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            with self.assertRaises(ValidationError) as _:
                AindBehaviorTaskLogicModelPre.model_validate_json(post_instance.model_dump_json())

    def test_pkg_version_update_forwards_coercion(self):
        pre_instance = SchemaVersionedModelPre()
        post_instance = SchemaVersionedModelPost()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                pre_updated = SchemaVersionedModelPost.model_validate_json(pre_instance.model_dump_json())
            except ValidationError as e:
                self.fail(f"Validation failed with error: {e}")

            self.assertEqual(pre_updated.version, post_instance.version, "Schema version was not coerced correctly.")

    def test_pkg_version_update_backwards_coercion(self):
        post_instance = SchemaVersionedModelPost()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            with self.assertRaises(ValidationError) as _:
                SchemaVersionedModelPre.model_validate_json(post_instance.model_dump_json())


if __name__ == "__main__":
    unittest.main()
