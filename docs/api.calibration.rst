calibration
-------------

Calibration Module
####################

The calibration module of this library keep a collection of models used to keep track of calibration metadata.

Every submodule has a single :py:class:`~aind_behavior_services.calibration.Calibration` class that is used to store the calibration metadata.
This class was written to be aligned to the Calibration class in `aind-data-schemas
<https://github.com/AllenNeuralDynamics/aind-data-schema/blob/2fd0e403bf46f0f1a47e5922c4228517e68376a3/src/aind_data_schema/components/devices.py#L274>`_ as to provide an easy way to map calibration data.

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


.. toctree::
   :maxdepth: 4

   api.calibration/aind_manipulator
   api.calibration/load_cells
   api.calibration/olfactometer
   api.calibration/water_valve
   api.calibration/treadmill


