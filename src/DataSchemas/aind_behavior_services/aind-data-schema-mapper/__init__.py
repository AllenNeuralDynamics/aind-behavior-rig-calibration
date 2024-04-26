try:
    import aind_data_schema
except ImportError as e:
    e.add_note(
        "The 'aind-data-schema' package is required to use this module. Install the optional dependencies defined in `project.toml' by running `pip install .[aind-data-schema-mapper]`"
    )
    raise



