import unittest
from datetime import datetime
from pathlib import Path

from aind_behavior_services.utils import run_bonsai_process


class BonsaiTests(unittest.TestCase):

    def test_deserialization(self):

        JSON_ROOT = Path("./local").resolve()
        workflow_props = {
            "aind_manipulator": JSON_ROOT / "aind_manipulator.json",
            "load_cells": JSON_ROOT / "load_cells.json",
            "olfactometer": JSON_ROOT / "olfactometer.json",
            "water_valve": JSON_ROOT / "water_valve.json",
        }
        completed_proc = run_bonsai_process(
            workflow_file=Path("./src/unit_tests.bonsai"),
            is_editor_mode=False,
            layout=None,
            additional_properties=workflow_props,
        )

        self.assertEqual(completed_proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
