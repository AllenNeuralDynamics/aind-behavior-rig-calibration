import datetime
import unittest
from typing import Literal

from pydantic import Field, TypeAdapter

from aind_behavior_services import AindBehaviorTaskLogicModel
from aind_behavior_services.base import DefaultAwareDatetime, SchemaVersionedModel
from aind_behavior_services.task_logic import TaskParameters
from aind_behavior_services.utils import format_datetime


class DefaultAwareDatetimeTest(unittest.TestCase):
    def setUp(self):
        self.type_adapter = TypeAdapter(DefaultAwareDatetime)
        self.datetime_naive = datetime.datetime(2021, 1, 1, 0, 0, 0, 0, tzinfo=None)
        self.datetime_utc = datetime.datetime(2021, 1, 1, 0, 0, 0, 0, tzinfo=datetime.timezone.utc)
        self.datetime_pst = datetime.datetime(
            2021, 1, 1, 0, 0, 0, 0, tzinfo=datetime.timezone(-datetime.timedelta(hours=8))
        )

    def test_timezone_naive(self):
        dt = self.type_adapter.validate_python(self.datetime_naive)
        self.assertIsNotNone(dt.tzinfo)
        self.assertEqual(self.type_adapter.validate_strings(format_datetime(self.datetime_naive)), dt)

    def test_timezone_utc(self):
        dt = self.type_adapter.validate_python(self.datetime_utc)
        self.assertEqual(dt.tzinfo, datetime.timezone.utc)
        self.assertEqual(dt, self.datetime_utc)
        self.assertEqual(self.type_adapter.validate_strings(format_datetime(self.datetime_utc)), dt)

    def test_timezone_pst(self):
        dt = self.type_adapter.validate_python(self.datetime_pst)
        self.assertEqual(dt.tzinfo, datetime.timezone(-datetime.timedelta(hours=8)))
        self.assertEqual(dt, self.datetime_pst)
        self.assertEqual(self.type_adapter.validate_strings(format_datetime(self.datetime_pst)), dt)


class SchemaVersionCoercionTest(unittest.TestCase):
    class AindBehaviorTaskLogicModelPre(AindBehaviorTaskLogicModel):
        version: Literal["0.0.1"] = "0.0.1"
        name: str = Field(default="Pre")
        task_parameters: TaskParameters = Field(default=TaskParameters(), validate_default=True)

    class AindBehaviorTaskLogicModelPost(AindBehaviorTaskLogicModel):
        version: Literal["0.0.2"] = "0.0.2"
        name: str = Field(default="Post")
        task_parameters: TaskParameters = Field(default=TaskParameters(), validate_default=True)

    class AindBehaviorTaskLogicModelMajorPost(AindBehaviorTaskLogicModel):
        version: Literal["0.1.0"] = "0.1.0"
        name: str = Field(default="Post")
        task_parameters: TaskParameters = Field(default=TaskParameters(), validate_default=True)

    class SchemaVersionedModelPre(SchemaVersionedModel):
        version: Literal["0.0.2"] = "0.0.2"
        aind_behavior_services_pkg_version: Literal["0.1.0"] = "0.1.0"

    class SchemaVersionedModelPost(SchemaVersionedModel):
        version: Literal["0.0.2"] = "0.0.2"
        aind_behavior_services_pkg_version: Literal["0.1.1"] = "0.1.1"

    class SchemaVersionedModelMajorPost(SchemaVersionedModel):
        version: Literal["0.0.2"] = "0.0.2"
        aind_behavior_services_pkg_version: Literal["1.1.0"] = "1.1.0"

    def test_version_update_forwards_coercion(self):
        pre_instance = self.AindBehaviorTaskLogicModelPre()
        post_instance = self.AindBehaviorTaskLogicModelPost()
        with self.assertLogs(None, level="WARNING") as cm:
            pre_updated = self.AindBehaviorTaskLogicModelPost.model_validate_json(pre_instance.model_dump_json())
            self.assertIn("Deserialized versioned field 0.0.1, expected 0.0.2. Will attempt to coerce.", cm.output[0])
            self.assertEqual(pre_updated.version, post_instance.version, "Schema version was not coerced correctly.")

    def test_version_update_backwards_coercion(self):
        post_instance = self.AindBehaviorTaskLogicModelPost()
        with self.assertLogs(None, level="WARNING") as cm:
            self.assertEqual(
                self.AindBehaviorTaskLogicModelPre.model_validate_json(post_instance.model_dump_json()).version,
                self.AindBehaviorTaskLogicModelPre().version,
            )
            self.assertIn("Deserialized versioned field 0.0.2, expected 0.0.1. Will attempt to coerce.", cm.output[0])

    def test_pkg_version_update_forwards_coercion(self):
        pre_instance = self.SchemaVersionedModelPre()
        post_instance = self.SchemaVersionedModelPost()
        with self.assertLogs(None, level="WARNING") as cm:
            pre_updated = self.SchemaVersionedModelPost.model_validate_json(pre_instance.model_dump_json())
            self.assertIn("Deserialized versioned field 0.1.0, expected 0.1.1. Will attempt to coerce.", cm.output[0])
            self.assertEqual(
                pre_updated.aind_behavior_services_pkg_version,
                post_instance.aind_behavior_services_pkg_version,
                "Schema version was not coerced correctly.",
            )

    def test_pkg_version_update_backwards_coercion(self):
        post_instance = self.SchemaVersionedModelPost()
        with self.assertLogs(None, level="WARNING") as cm:
            self.assertEqual(
                self.SchemaVersionedModelPre.model_validate_json(post_instance.model_dump_json()).version,
                self.SchemaVersionedModelPre().version,
            )
            self.assertIn("Deserialized versioned field 0.1.1, expected 0.1.0. Will attempt to coerce.", cm.output[0])


if __name__ == "__main__":
    unittest.main()
