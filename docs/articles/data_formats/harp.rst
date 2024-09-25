Harp
------------------------------------------

Version
#############
0.1.0-draft

Introduction
##############

While Harp data is largely used for behavior experiments, it is not limited to this modality. As a result, the current standard is scoped to the logging at the level of single Harp devices. The reason for this decision will hopefully become clear as we describe the format and some of the rationale behind it.

Most of the Harp-related concepts mentioned here will be expanded in the `documentation of the protocol <https://harp-tech.org/protocol/BinaryProtocol-8bit.html>`_.

We will strictly follow the logging standards defined by `Harp <https://harp-tech.org/articles/python.html#data-models>`_. This decision is justified by the following reasons:

- Affords the ability to not only use the same data format within our organization but also to share data with other groups that use Harp;
- Affords the ability to reuse common `data ingesting tools maintained by others <https://pypi.org/project/harp-python/0.2.0/>`_. Since it is an open-source community standard, we also have the ability to contribute to the development of these tools if we so wish;
- Affords re-usability of data acquisition, QC and processing pipelines that can be centralized and validated by us and potentially used by others.

Format specification
####################################

One of the main advantages of using a standardized binary communication protocol is that logging data from harp devices can be largely generalized. In theory, we could simply dump the binary data from the device into a single file and call it a day. However this is not always the most convenient way to log data. For instance, if one is interested in ingesting only a subset of messages (e.g. only the messages from a particular sensor or pin), then the previous approach would require a post-processing step to filter out the messages of interest.
Furthermore, each address, as per harp protocol spec, has potentially different data formats (e.g. ``U8`` vs ``U16``) or even different lengths if array registers are involved. This can make it very tedious to parse and analyze a binary file offline, since we will have to examine the header of each and every message in the file to determine how to extract its contents.

This analysis could be entirely eliminated if we knew that all messages in the binary file had the same format. For any Harp device, the payload stored in a specific register will have a fixed type and length. This means that to ensure our simplifying assumption it is enough to save each message from a specific register into a different file (aka de-multiplexing strategy).

Thus, for each device, the container of all data will be a single directory with the extension ``<>.harp``. This directory will contain the following files:

.. code-block:: none

    📦<Device>.harp
    ┣ 📜<DeviceName>_0.bin
    ┣ 📜<DeviceName>_1.bin
    ┣ ...
    ┣ 📜<DeviceName>_<Reg>.bin
    ┗ 📜device.yml (Optional)

where:

- ``<DeviceName>`` will be derived from the ``device.yml`` metadata file that fully defines the device and can be found in the repository of each device (`e.g. <https://raw.githubusercontent.com/harp-tech/device.behavior/main/device.yml>`_). This file can be seen as the "ground truth" specification of the device. It is used to automatically generate documentation, interfaces and data ingestion tools.
- ``<Device>`` should match the name of the device in the ``rig.json`` schema file;
- ``<Reg>`` is the register number that is logged in the binary file.

The optional ``device.yml`` file
++++++++++++++++++++++++++++++++

Including the ``device.yml`` file that corresponds to the device interface used to log the device's data is recommended. Currently, this is not mandatory, but as ecosystem adoption progresses and tools improve, it will likely become a standard requirement. Note that while the ``device.yml`` file specifies the targeted hardware, firmware, and core versions, it does not guarantee that the device from which data was acquired is running those versions. This metadata should instead be queried directly from the corresponding device's registers(`see protocol core registers <https://harp-tech.org/protocol/Device.html#table---list-of-available-common-registers>`_)

Optional logging of commands
++++++++++++++++++++++++++++++++

A critical aspect of using the Harp protocol is that for each ``Write`` message received by the device from the PC host, the client will echo back a Write message timestamped by the embedded device. This assumes that all messages issued by the host are received by the device and not lost in transmission. However, this is not guaranteed. In case of a lost message, the host will not receive the echo back and cannot confirm that the message was received by the device.

To perform post-hoc quality control, we recommend also logging ``Commands``. Since ``Commands`` are also HarpMessage types, they can be logged in the same format as data from devices. We also recommend appending a software timestamp to each ``Command`` message to facilitate pairing requests with responses post-hoc.


Application notes
#####################

All harp devices, regardless of their specific application, are expected to be logged according to the following standards:

Clock Synchronization
+++++++++++++++++++++++

We will only consider two operational modes for devices used in the AIND: ``Standalone`` and ``Synchronized``

- In ``Standalone`` mode the Harp device is not subordinate to a distributed clock, and all messages are timestamped by the device's internal clock. This mode can be used if only a single Harp device is used during experiment acquisition.
- In ``Synchronized`` mode, the Harp device is subordinate to a distributed clock, and all messages are timestamped by the distributed clock. This mode should be used when multiple Harp devices are used during experiment acquisition. In each experiment, there shall be a single clock generator source (e.g. `WhiteRabbit device <https://github.com/AllenNeuralDynamics/harp.device.white-rabbit>`_) to which all devices are connected. This source device is logged like any other Harp device.


Interfacing with Bonsai
+++++++++++++++++++++++++

The following points will describe recommendations and recipes for logging data from harp devices using `Bonsai programming language <https://bonsai-rx.org/>`_. We will assume a basic `understanding of the Bonsai programming language <https://bonsai-rx.org/docs/>`_, and `how to interface with Harp devices from it <https://harp-tech.org/articles/intro.html>`_.


Instructions on how to log data from a Harp device using Bonsai can be found in the `Harp Bonsai interface docs <https://harp-tech.org/articles/logging.html#groupbyregister>`_.

.. warning::
    In your experiments, always validate that your logging routine has fully initialized before requesting a reading dump from the device. Failure to do so may result in missing data.

.. note::
    In the future we will update these recipes to also provide AIND specific examples.


It is critical that the messages logged from the device are sufficient to reconstruct its state history. For that to be true, we need to know the initial state of all registers. This can be asked via a special register in the protocol core: `OperationControl <https://harp-tech.org/protocol/Device.html#r_operation_ctrl-u16--operation-mode-configuration>`_. This register has a single bit that, when set, will trigger the device to send a dump all the values of all its registers.

- To the previous example, in a different branch:
- Add a ``Timer`` operator with its ``DueTime`` property set to 2 seconds. This will mimic the delayed start of an experiment.
- Add a ``CreateMessage(Bonsai.Harp)`` operator after the ``Timer``
- Select ``OperationControlPayload`` under ``Payload``. Depending on your use case, you might want to change some of the settings, but we recommend:
  - ``DumpRegisters`` set to ``True`` (Required for the dump)
  - ``Heartbeat`` set to ``True`` (Useful to know the device is still alive)
  - ``MuteReplies`` set to ``False``
  - ``OperationLed`` set to ``True``
  - ``OperationMode`` set to ``Active``
  - ``VisualIndicator`` set to ``On``
- Add a ``Multicast`` operator to send the message to the device

.. raw:: html

   <details>
   <summary><a>Bonsai example workflow</a></summary>

.. code-block:: xml

    <?xml version="1.0" encoding="utf-8"?>
    <WorkflowBuilder Version="2.8.1"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xmlns:rx="clr-namespace:Bonsai.Reactive;assembly=Bonsai.Core"
                    xmlns:harp="clr-namespace:Bonsai.Harp;assembly=Bonsai.Harp"
                    xmlns="https://bonsai-rx.org/2018/workflow">
    <Workflow>
        <Nodes>
        <Expression xsi:type="Combinator">
            <Combinator xsi:type="rx:Timer">
            <rx:DueTime>PT2S</rx:DueTime>
            <rx:Period>PT0S</rx:Period>
            </Combinator>
        </Expression>
        <Expression xsi:type="harp:CreateMessage">
            <harp:MessageType>Write</harp:MessageType>
            <harp:Payload xsi:type="harp:CreateOperationControlPayload">
            <harp:OperationMode>Active</harp:OperationMode>
            <harp:DumpRegisters>false</harp:DumpRegisters>
            <harp:MuteReplies>false</harp:MuteReplies>
            <harp:VisualIndicators>Off</harp:VisualIndicators>
            <harp:OperationLed>Off</harp:OperationLed>
            <harp:Heartbeat>Disabled</harp:Heartbeat>
            </harp:Payload>
        </Expression>
        <Expression xsi:type="MulticastSubject">
            <Name>BehaviorCommands</Name>
        </Expression>
        </Nodes>
        <Edges>
        <Edge From="0" To="1" Label="Source1" />
        <Edge From="1" To="2" Label="Source1" />
        </Edges>
    </Workflow>
    </WorkflowBuilder>

.. raw:: html

   </details>


Finally, commands to the device can be logged in the exact same way as replies. However, in order to facilitate post-hoc quality control, we recommend appending a software timestamp to each ``Command`` message. This can be done by `"injecting" a timestamp into the message payload <https://harp-tech.org/articles/message-manipulation.html#injecting-or-modifying-message-timestamps>`_ before logging. We recommend using high frequency events from a single device as a `source of "the latest timestamp" to be used in the Command message <https://harp-tech.org/articles/message-manipulation.html#timestamping-generic-data>`_. We should stress that these timestamps should not be used for analysis that require precise and accurate synchronization, as they are not synchronized with the distributed clock.


Relationship to aind-data-schema
#################################

Most fields tracked in ``rig.json`` can be easily extracted from the device's read-dump. It is likely that helper methods will be provided in the future to automate this conversion. For now, refer to the `protocol's core registers <https://github.com/harp-tech/protocol/blob/main/Device.md#table---list-of-available-common-registers>`_ to extract the necessary information.

File Quality Assurances
##########################
By virtue of implementing the Harp communication and synchronization protocol the following should be true:

- Each data set should, at most, have a device as a source of the synchronized clock.
- All messages from the device to the computer host should be logged. Once a message is successfully parsed, no more processing and/or filtering of the data stream will be done prior to logging.
- All data from a single device will include the initial state of all registers. This can be achieved by setting the ``DumpRegisters`` bit in the ``OperationControl`` register. Given that this is true, inside the container folder, one file per register of the device is expected to be found with a minimum of one message in each file.
- If Commands are logged, for each message sent to the device, a corresponding message should exist in the logged data from the harp device. The type of the message in the Command will match the type of the reply from the device.
- If multiple devices are used, all data is assumed to be synchronized at acquisition time.