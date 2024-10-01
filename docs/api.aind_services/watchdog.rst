Watchdog
-------------

This module provides a wrapper around the `aind-watchdog-service <https://github.com/AllenNeuralDynamics/aind-watchdog-service>`_. This service is used to monitor new data produced by a local rig and upload it via the `aind-data-transfer service <https://github.com/AllenNeuralDynamics/aind-data-transfer>`_.

Deployment
###########

The module relies on a valid instance of the watchdog executable running on the local machine.

This module will consider the following defaults:

 - The watchdog executable will be located at `%PROGRAMDATA%/aind-watchdog-service/watchdog.exe`
 - The `manifests` and `completed` directories (used by the watchdog.exe to keep track of new and completed jobs, respectively), will be located at `%PROGRAMDATA%/aind-watchdog-service/manifests` and `%PROGRAMDATA%/aind-watchdog-service/completed`, respectively.

While any of these settings can be changed, it is recommended to use the defaults as it allows all further customization to be handled solely by the python module.

The watchdog executable can be downloaded from the `releases page <https://github.com/AllenNeuralDynamics/aind-watchdog-service/releases>`_ and setup as per provided instructions to run at system startup.

Alternatively, a provided powershell script can automatically deploy the service (`./scripts/setup_watchdog.ps1``):

.. literalinclude:: ../../scripts/setup_watchdog.ps1
      :language: ps1


Use
#######

The module provides a single entry point to the watchdog service: :py:class:`~aind_behavior_services.launcher.watchdog_service.WatchdogClient`.

In general, users are expected to create an instance of the class e.g.:

.. code-block:: python

   from aind_behavior_services.launcher import watchdog_service
   import datetime

    watchdog = watchdog_service.WatchdogClient(
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



