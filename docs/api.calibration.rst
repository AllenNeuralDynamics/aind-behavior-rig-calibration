calibration
-------------

Calibration Module
####################

The calibration module of this library is used to generate the metadata necessary configure and run calibration workflows for different assets/devices.

The metadata follows the general logic of the library by implementing the three core classes:
   - :py:class:`~aind_behavior_services.session.AindBehaviorSessionModel`
   - :py:class:`~aind_behavior_services.rig.AindBehaviorRigModel`
   - :py:class:`~aind_behavior_services.task_logic.AindBehaviorTaskLogicModel`

A fourth class :py:class:`~aind_behavior_services.calibration.Calibration`,
specific to the Calibration module, is also implemented to keep track of the calibration metrics.
This class was written to be aligned to the Calibration class in `aind-data-schemas
<https://github.com/AllenNeuralDynamics/aind-data-schema/blob/2fd0e403bf46f0f1a47e5922c4228517e68376a3/src/aind_data_schema/components/devices.py#L274>`_.
An application example will be provided below.

While we use the base :py:class:`~aind_behavior_services.session.AindBehaviorSessionModel` class to keep track of the session metadata,
both :py:class:`~aind_behavior_services.rig.AindBehaviorRigModel` and :py:class:`~aind_behavior_services.task_logic.AindBehaviorTaskLogicModel` are
expected to be sub-classed to specify the necessary dependencies of the calibration workflow.

Sub-classing :py:class:`~aind_behavior_services.calibration.Calibration`
##########################################################################

Sub-classing :py:class:`~aind_behavior_services.calibration.Calibration` boils down to providing a subtype of the `input` and `output` fields.
These fields are expected to be of a sub-type of `~pydantic.BaseModel` and define the structure of the calibration outcome.
Conceptually, `input` is the pre-process data that resulted from the calibration workflow (i.e. the weight of delivered water),
whereas `output` is used to represent a post-processed version of the calibration outcome (e.g. a linear model that relates valve-opening times to water volume).

An example of a sub-class of `Calibration` is provided below:

.. code-block:: python

   from pydantic import BaseModel, Field
   from typing import List, Literal
   from aind_behavior_services.calibration import Calibration


   class BarContainer(BaseModel):
      baz: string = Field(..., description="Baz value")
      bar: float = Field(..., description="Bar value")


   class DeviceCalibrationInput(BaseModel):
      measured_foo: List[int] = Field(..., description="Measurements of Foo")
      bar_container: List[BarContainer] = Field(..., description="Bar container")


   class DeviceCalibrationOutput(BaseModel):
      param_a = float = Field(default=1, description="Parameter A")
      param_b = float = Field(default=0, description="Parameter B")


   class DeviceCalibration(Calibration):
      device_name: Literal["MyDevice"] = "MyDevice"
      description: Literal["Stores the calibration of a device"] = "Stores the calibration of a device"
      input: DeviceCalibrationInput = Field(..., title="Input of the calibration")
      output: DeviceCalibrationOutput = Field(..., title="Output of the calibration")

Sub-classing :py:class:`~aind_behavior_services.rig.AindBehaviorRigModel`
##########################################################################

We adopt the following pattern to sub-class the :py:class:`~aind_behavior_services.rig.AindBehaviorRigModel` class:

.. code-block:: python

   from aind_behavior_services.rig import AindBehaviorRigModel, Device

   RIG_VERSION = "1.0.0" # Use SemVer

   class FooDevice(Device):
      calibration: DeviceCalibration = Field(..., title="Calibration of the device foo")


   class CalibrationRig(AindBehaviorRigModel):
      version: Literal[RIG_VERSION] = RIG_VERSION
      device_foo: FooDevice = Field(..., title="Device Foo")
      device_bar: Device = Field(..., title="Device Bar")


For an example see :py:class:`aind_behavior_services.calibration.olfactometer.CalibrationRig`.



Sub-classing :py:class:`~aind_behavior_services.task_logic.AindBehaviorTaskLogicModel`
########################################################################################

The same way a :py:class:`~aind_behavior_services.task_logic.AindBehaviorTaskLogicModel` is used to define
the settings to run a behavior task, it is also used to define the settings to run a calibration workflow.
It will thus follow an identical sub-classing pattern:


.. code-block:: python

   from aind_behavior_services.task_logic import AindBehaviorTaskLogicModel, TaskParameters

   TASK_LOGIC_VERSION = "0.1.0"

   class CalibrationParameters(TaskParameters):
      n_iterations: int = Field(default=10, description="Number of iterations to run the calibration")
      channels_to_calibrate: List[Literal[1,2,3]] = Field(default=[1], description="List of channels to calibrate")

   class CalibrationLogic(AindBehaviorTaskLogicModel):
      name: Literal["CalibrationLogic"] = "CalibrationLogic
      version: Literal[TASK_LOGIC_VERSION] = TASK_LOGIC_VERSION
      task_parameters: CalibrationParameters = Field(default=CalibrationParameters(), title="Task parameters", validate_default=True)


For an example see :py:class:`aind_behavior_services.calibration.olfactometer.CalibrationLogic`.



.. toctree::
   :maxdepth: 4

   api.calibration/aind_manipulator
   api.calibration/load_cells
   api.calibration/olfactometer
   api.calibration/water_valve
   api.calibration/treadmill


