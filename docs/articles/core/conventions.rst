Standard conventions
---------------------

Version
#############
0.1.0-draft

Introduction
#############

The goal of this document is NOT to be exhaustive and opinionated. Instead, it should include a minimal list of common patterns that can be easily referenced and reused across all data formats standards guaranteeing a minimal level of consistency and quality.

Filenames
####################

In general, filename conventions will be defined by the specific data format standard. However, some general rules will be enforced:

- Filenames must not contain spaces or special characters. `Use this as a reference for special characters <https://en.wikipedia.org/wiki/Filename#Reserved_characters_and_words>`_.
- "Underscore" `_` should be used instead of "-" or any other special character to separate words.
- Filenames should always contain a file extension. If no extension is provided, the file will be considered a flat binary file.
- ANY file name can be suffixed with a ``datetime``. This suffix will ALWAYS be the last suffix in the filename, in case multiple suffixes are used, and will follow the ISO 8601 format and always be timezone aware, or UTC if no tz information is provided. If a `datetime` field is added we will adopt the format `YYYY-MM-DDTHHMMSS` e.g. `2023-12-25T133015` (`Reference <https://github.com/neuroinformatics-unit/NeuroBlueprint/issues/31>`_). See the :ref:`datetime <datetime_target>`: section for more details.

- As an example, if two files (``data_stream.bin``) are generated as part of two different acquisition `streams <https://aind-data-schema.readthedocs.io/en/latest/session.html>`_:

.. code-block:: none

    📂Modality
    ┣ 📜data_stream_2023-12-25T133015Z.bin
    ┗ 📜data_stream_2023-12-25T145235Z.bin

- This rule can be generalized to container-like file formats by adding the suffix to the container:

.. code-block:: none

    📂Modality
    ┣ 📂FileContainer_2023-12-25T133015Z
    ┃ ┣ 📜file1.bin
    ┃ ┗ 📜file2.csv
    ┣ 📂FileContainer_2023-12-25T145235Z
    ┃ ┣ 📜file1.bin
    ┗ ┗ 📜file2.csv

.. _datetime_target:

``Datetime``
##############

All ``datetime`` used in data formats should follow the `ISO 8601 <https://en.wikipedia.org/wiki/ISO_8601>`_ standard. This standard is widely used and supported by most programming languages and libraries. All `datetime` are expected to be timezone aware, or UTC if no timezone information is provided. We encourage the following pattern:

- ``YYYY-MM-DDTHHMMSS`` e.g. ``2023-12-25T133015``
- ``YYYY-MM-DDTHHMMSSZ`` e.g. ``2023-12-25T133015Z``
- ``YYYY-MM-DDTHHMMSS±HHMM`` e.g. ``2023-12-25T133015+1200``

The following examples show how to parse these formats in Python:

.. code-block:: python

    import datetime

    implicit_utc = "2023-12-25T133015"
    utc = "2023-12-25T133015Z"
    tz_aware = "2023-12-25T133015+1200"

    print(datetime.datetime.fromisoformat(implicit_utc))
    #  2023-12-25 13:30:15
    print(datetime.datetime.fromisoformat(utc))
    #  2023-12-25 13:30:15+00:00
    print(datetime.datetime.fromisoformat(tz_aware))
    #  2023-12-25 13:30:15+12:00

Tabular formats
####################

The supported tabular formats are:

Comma-separated values (``CSV``)
++++++++++++++++++++++++++++++++++++

``CSV`` files will follow a subset of the `RFC 4180 <https://tools.ietf.org/html/rfc4180>`_ standard.
The following rules will be enforced:

- The first row will always be the header row.
- The separator will always be a comma (``,``).
- The file will always be encoded in UTF-8.
- The extension of the file will always be ``.csv``.