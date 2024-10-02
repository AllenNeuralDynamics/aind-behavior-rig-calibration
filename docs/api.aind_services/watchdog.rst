Watchdog
-------------

This module provides a wrapper around the `aind-watchdog-service <https://github.com/AllenNeuralDynamics/aind-watchdog-service>`_. This service is used to monitor new data produced by a local rig and upload it via the `aind-data-transfer service <https://github.com/AllenNeuralDynamics/aind-data-transfer>`_.

Deployment
###########

The module relies on a valid instance of the watchdog executable running on the local machine.

This module will consider the following defaults:

 - The watchdog executable will be located at %WATCHDOG_EXE% (this is an environment variable that should be set to the path of the watchdog executable).

 - The `WatchConfig` serialized model will be located at %WATCHDOG_CONFIG% (this is an environment variable that should be set to the path of the serialized model).
    - If this file does not exist it will be created with the defaults defined in :py:class:`~aind_behavior_services.launcher.watchdog_service.WatchdogClient`.

While any of these settings can be changed, it is recommended to use the defaults as it allows all further customization to be handled solely by the python module.

The watchdog executable can be downloaded from the `releases page <https://github.com/AllenNeuralDynamics/aind-watchdog-service/releases>`_ but we strongly recommended using the automatic deployment provided by SIPE.

#######

The module provides a single entry point to the watchdog service: :py:class:`~aind_behavior_services.launcher.watchdog_service.WatchdogClient`.

In general, users are expected to create an instance of the class e.g.:

.. code-block:: python

   from aind_behavior_services.launcher import watchdog_service
   import datetime

    watchdog = watchdog_service.WatchdogService(
        project_name="Cognitive flexibility in patch foraging",  # the project name is required by the aind-transfer-service
        schedule_time=datetime.time(hour=20)  # schedules the transfer time to 8pm
    )

Once the instance is created, the user can interface with the service using the provided class methods. For example, to create a manifest file from an already existing :py:class:`~aind-data-schema.core.session.Session` model object:

.. code-block:: python

    from aind_behavior_services.core.session import Session
    session: Session #  this should be a valid session object
    watchdog.create_manifest_config(
        ".\src_path",
        "\\allen\aind\dst_path",
        session)


For an implementation example see the :py:class:`~aind_behavior_services.launcher.Launcher` class.


.. automodule:: aind_behavior_services.launcher.watchdog_service
   :members:
   :undoc-members:
   :show-inheritance:



