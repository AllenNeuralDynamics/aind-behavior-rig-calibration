import pydantic


def build_json_schema(model: pydantic.BaseModel):
    """Build a JSON schema model from a pydantic model"""
    return model.model_json_schema(indent=2)
