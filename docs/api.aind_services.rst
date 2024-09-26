aind_services
-------------

AIND Services Module
####################

The calibration module of this library is used to interface with AIND provided libraries and repositories.
While we will try to keep this library up to date, it is recommended to check the original repositories for the most recent updates.

A list of services relevant for this library include:
   - `aind-data-schema <https://github.com/AllenNeuralDynamics/aind-data-schema>`_
   - `aind-data-schema-models <https://github.com/AllenNeuralDynamics/aind-data-schema-models>`_
   - `aind-watchdog-service <https://github.com/AllenNeuralDynamics/aind-watchdog-service>`_
   - `aind-slims-api <https://github.com/AllenNeuralDynamics/aind-slims-api>`_
   - `aind-data-mapper <https://github.com/AllenNeuralDynamics/aind-metadata-mapper>`_


We will generally try to wrap the services provided by these repositories into a more user-friendly and opinionated interface that can be used by the Aind Behavior Services library and other repositories.

We will also try to scope all dependencies of the related to AIND Services to its own optional dependency list in the `./pyproject.toml` file of this repository. Therefor, in order to use this module, you will need to install these optional dependencies by running:

```pip install .[aind-services]```

Feedback and contributions are welcome!


.. toctree::
   :maxdepth: 2

   api.aind_services/watchdog
   api.aind_services/data_mapper
   api.aind_services/helpers
