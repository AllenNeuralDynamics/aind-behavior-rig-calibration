import logging
import unittest

from aind_behavior_services.launcher import resource_manager_service, watchdog_service


class LauncherServicesTests(unittest.TestCase):

    def test_resource_manager_service(self):

        logger = logging.getLogger(__name__)
        resource_manager = resource_manager_service.ResourceManager(logger)

        resource_manager.add_constraint(
            resource_manager_service.Constraint(
                name="test_constraint",
                constraint=lambda: True,
                fail_msg_handler=lambda: "Constraint failed."
                )
        )

        self.assertTrue(resource_manager.evaluate_constraints())

        resource_manager.add_constraint(
            resource_manager_service.Constraint(
                name="test_constraint",
                constraint=lambda: False,
                fail_msg_handler=lambda: "Constraint failed."
                )
        )

        resource_manager.add_constraint(resource_manager)
        self.assertFalse(resource_manager.evaluate_constraints())

    def test_resource_manager_service_constraint(self):

        constraint = resource_manager_service.Constraint(
            name="test_constraint",
            constraint=lambda x: x,
            fail_msg_handler=lambda: "Constraint failed.",
            args=[True]
        )

        self.assertTrue(constraint(), True)

        constraint = resource_manager_service.Constraint(
            name="test_constraint",
            constraint=lambda x: x,
            fail_msg_handler=lambda: "Constraint failed.",
            args=[False]
        )
        self.assertFalse(constraint(), False)

    def test_watchdog_service(self):
        _ = watchdog_service.WatchdogService(logger=logging.getLogger(__name__))


if __name__ == "__main__":
    unittest.main()
