import unittest

from aind_behavior_services.launcher import (
    app_service,
    data_mapper_service,
    data_transfer_service,
    resource_monitor_service,
)


class LauncherServicesTests(unittest.TestCase):
    def test_resource_monitor_service(self):
        resource_monitor = resource_monitor_service.ResourceMonitor()

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
        _ = data_transfer_service.WatchdogDataTransferService(destination="mock_path", validate=False)

    def test_app_service(self):
        _ = app_service.BonsaiApp("test.bonsai")

    def test_data_mapper_service(self):
        _ = data_mapper_service.AindDataSchemaSessionDataMapper()


if __name__ == "__main__":
    unittest.main()
