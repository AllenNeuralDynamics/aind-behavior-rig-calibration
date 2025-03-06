Video
------------------------------------------

Version
#############
0.1.0-draft

Introduction
##############

This document describes the standards for acquiring video data from behavior experiments. The goal is to ensure that the data is correctly acquired, logged, and stored in a way that is compatible with AIND's data processing pipelines. We will draw the line on including metadata that relates to the video data itself and NOT to the hardware or software that acquired it. This is to ensure that the data format is self-contained, maintainable and potentially reusable by other applications.

Format specification
####################################

Following SciComp standards, video data from behavior experiments should be saved to the ``behavior-videos`` modality folder.

Inside this folder, each camera should have its own directory, named ``<CameraName>``. Inside each camera folder, there should be two files: ``video.<extension>`` and ``metadata.csv``. The ``video.<extension>``` file should contain the video data, and the ``metadata.csv`` file should contain the metadata for the video.

``<CameraName>`` is expected to match the name defined in the rig metadata file (``rig.json``) from `aind-data-schema <https://aind-data-schema.readthedocs.io/en/latest/rig.html>`_.

The folder structure will thus be:

.. code-block:: none

    📦behavior-videos
    ┣ 📂BodyCamera
    ┃ ┣ 📜metadata.csv
    ┃ ┗ 📜video.mp4
    ┗ 📂FaceCamera
    ┃ ┣ 📜metadata.csv
    ┃ ┗ 📜video.mp4


If multiple streams from the same camera are acquired in the same session, an optional ``datetime`` suffix can be added to the container's name:

.. code-block:: none

    📦behavior-videos
    ┣ 📂BodyCamera_2023-12-25T133015Z
    ┃ ┣ 📜metadata.cs
    ┃ ┗ 📜video.mp4
    ┗ 📂BodyCamera_2023-12-25T145001Z
    ┃ ┣ 📜metadata.csv
    ┃ ┗ 📜video.mp4

The metadata file is expected to contain the following columns:

- ``ReferenceTime``` - Time of the trigger given by hardware (e.g. Harp)

- ``CameraFrameNumber`` – Frame counter given by the camera API or manually added by user (e.g. using OS counter for webcams)

- ``CameraFrameTime`` – Frame acquisition time given by the camera API or manually added by the user (e.g. using OS scheduler for webcams).


As for the video, since the format will depend on the scientific question and software/hardware constrains, we will not enforce a specification. However, we strongly discourage the use of RAW, uncompressed data, and should the user not have a preference, we suggest the follow default:

Since this format will depend on the scientific question and software/hardware constrains, we will not enforce a specific format. However, if the user does not have a preference we suggest using the defaults defined in:
``~aind_behavior_services.rig.VideoWriterFfmpeg``

or

- Use mp4 container
- Acquire without any gamma correction
- Use ``ffmpeg`` with the encoding codec string for online encoding (optimized for compression quality and speed) set to the default values defined in :py:attr:`~aind_behavior_services.rig.FFMPEG_OUTPUT_8BIT` and :py:attr:`~aind_behavior_services.rig.FFMPEG_INPUT`:

The following encoding codec string can be used for offline re-encoding (optimized for quality and size):

- output arguments: ``-vf "scale=out_color_matrix=bt709:out_range=full:sws_dither=none,format=yuv420p10le,colorspace=ispace=bt709:all=bt709:dither=none,scale=out_range=tv:sws_dither=none,format=yuv420p" -c:v libx264 -preset veryslow -crf 18 -pix_fmt yuv420p -metadata author="Allen Institute for Neural Dynamics" -movflags +faststart+write_colr``

.. warning::

  This pipeline has been designed and tested with monochrome videos with the raw pixel format ``gray``. For color videos, the arguments might need to be altered to match the color space of the input.

  For higher bit depth (more than 8 bit) recordings, change the output arguments of the online, first stage, encoding to :py:attr:`~aind_behavior_services.rig.FFMPEG_OUTPUT_16BIT`
  This is almost the same, except the intermediate color representation is 48 bits per pixel instead of 24.

Application notes
#####################

We currently support the following cameras:
    - ``Blackfly S BFS-U3-16S2M``
    - ``Blackfly S BFS-U3-04S2M``

Additional cameras could be supported but the user should provide the necessary information to integrate it with the current pipeline.

.. warning::

    It is the user's responsibility to ensure that:
    - The camera is correctly calibrated and that the settings are appropriate for the experiment.

    - Unless there is a reason not to, the default logging pattern should always follow the following logic: (Stop trigger if needed) -> Start logging -> Start Camera -> Start Trigger -Acquire data -> Stop Trigger -> Stop Logging. This guarantees that all relevant events are recorded.

    - Trigger generation only starts AFTER the camera hardware has been initialized. This is to ensure that the camera is ready to receive the first trigger signal.

    - For each trigger of the trigger source (e.g. Harp Behavior board) a corresponding camera exposure should occur. One example where this can be violated is if the set exposure is greater than the trigger frequency.

    - In absence of dropped frames (defined as skips in the FrameNumber 1) the metadata.csv file is expected to be aligned with the video file.

    - (Optional) Start trigger and Stop trigger events should be available for QC.

    - (Optional) The logs of all triggers (regardless of whether they are logged in the metadata.csv) should be saved for redundancy.


Acquisition and Logging
+++++++++++++++++++++++++++++

Acquisition can be achieved using Bonsai. An operator that instantiates the camera can be found in `AllenNeuralDynamics.Core package <https://allenneuraldynamics.github.io/Bonsai.AllenNeuralDynamics/api/AllenNeuralDynamics.Core.AindSpinnakerCapture.html>`_.
This operator is a wrapper around the Spinnaker SDK and provides a simple interface to acquire video data. Since it forces the camera into the correct settings (e.g. Trigger mode, disabled gamma correction, etc...), it guarantees that camera metadata is static and thus easier to track.

Logging can be implemented via the `FFMPEG operator <https://allenneuraldynamics.github.io/Bonsai.AllenNeuralDynamics/api/AllenNeuralDynamics.Core.FfmpegVideoWriter.html>`_.

While we suggest using the aforementioned recipes, the user is free to use any software that can acquire video data, provided it is validated and logged in the correct format.

Relationship to aind-data-schema
##################################
``<CameraName>`` is expected to match the name defined in the rig metadata file (``rig.json``). Several fields in the metadata can be automatically extracted from this file format (e.g. start and stop of the stream, resolution of the video). However, the user should ensure that any data pertaining to the hardware configuration (e.g. camera model, exposure time, gain, camera position, etc...) is logged independently from this file format herein described. In the case of this repository, the metadata will be defined in the :py:class:`~aind_behavior_services.rig.AindBehaviorRigModel` instances.

File Quality Assurances
###########################

The following features should be true if the data asset is to be considered valid:

- The number of frames in the encoded video should match the number of recorded frames and the number of frames in the metadata.

- Check if dropped frames occurred. This should be done in two ways:

  - The difference between adjacent ``FrameNumber`` is always 1;

  - The difference between adjacent ``Seconds`` and adjacent ``FrameTime`` should be very close (I would suggest a threshold of 0.5ms for now);

    .. note::
        While dropped frames are not ideal, they do not necessarily invalidate the data. However, the user should be aware of the potential consequences and/or ways to correct the data asset.

- If using a stable frame rate (this should be inferred from a rig configuration file), the average frame rate should match the theoretical frame rate;

- (optional) If the optional start and stop events are provided, the following temporal order should be asserted: ``All(StartTrigger < Frames  < StopTrigger>)``
