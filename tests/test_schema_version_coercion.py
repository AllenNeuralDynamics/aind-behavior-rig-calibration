import unittest
from typing import Literal

from aind_behavior_services import AindBehaviorTaskLogicModel
from pydantic import ValidationError

version_pre: str = "0.0.1"
version_post: str = "0.0.2"


class AindBehaviorRigModelPre(AindBehaviorTaskLogicModel):
    schema_version: Literal[version_pre] = version_pre
    describedBy: str = "Foo"


class AindBehaviorRigModelPost(AindBehaviorTaskLogicModel):
    schema_version: Literal[version_post] = version_post
    describedBy: str = "Foo"


class SchemaVersionCoercionTest(unittest.TestCase):

    def test_version_update_coercion(self):

        pre_instance = AindBehaviorRigModelPre()
        post_instance = AindBehaviorRigModelPost()

        with self.assertRaises(ValidationError):
            pre_updated = AindBehaviorRigModelPost.model_validate_json(pre_instance.model_dump_json())

        self.assertEqual(
            pre_updated.schema_version, post_instance.schema_version, "Schema version was not coerced correctly."
        )


if __name__ == "__main__":
    unittest.main()
