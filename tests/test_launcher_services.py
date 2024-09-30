import logging
import unittest

from aind_behavior_services.launcher import resource_monitor_service, watchdog_service


class LauncherServicesTests(unittest.TestCase):
    def test_resource_monitor_service(self):
        logger = logging.getLogger(__name__)
        resource_monitor = resource_monitor_service.ResourceMonitor(logger)

        resource_monitor.add_constraint(
            resource_monitor_service.Constraint(
                name="test_constraint", constraint=lambda: True, fail_msg_handler=lambda: "Constraint failed."
            )
        )

        self.assertTrue(resource_monitor.evaluate_constraints())

        resource_monitor.add_constraint(
            resource_monitor_service.Constraint(
                name="test_constraint", constraint=lambda: False, fail_msg_handler=lambda: "Constraint failed."
            )
        )

        resource_monitor.add_constraint(resource_monitor)
        self.assertFalse(resource_monitor.evaluate_constraints())

    def test_resource_monitor_service_constraint(self):
        constraint = resource_monitor_service.Constraint(
            name="test_constraint", constraint=lambda x: x, fail_msg_handler=lambda: "Constraint failed.", args=[True]
        )

        self.assertTrue(constraint(), True)

        constraint = resource_monitor_service.Constraint(
            name="test_constraint", constraint=lambda x: x, fail_msg_handler=lambda: "Constraint failed.", args=[False]
        )
        self.assertFalse(constraint(), False)

    def test_watchdog_service(self):
        _ = watchdog_service.WatchdogService(logger=logging.getLogger(__name__))


if __name__ == "__main__":
    unittest.main()
