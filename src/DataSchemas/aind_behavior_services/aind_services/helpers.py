from typing import TypeVar, Type, Any, Iterable, Dict, List, Union, get_args
import pydantic

from aind_behavior_services.rig import CameraController, CameraTypes, AindBehaviorRigModel

T = TypeVar("T")


def get_cameras(
    rig_instance: AindBehaviorRigModel, exclude_without_video_writer: bool = True
) -> Dict[str, CameraTypes]:
    cameras: dict[str, CameraTypes] = {}
    camera_controllers = get_fields_of_type(rig_instance, CameraController)

    for controller in camera_controllers:
        if exclude_without_video_writer:
            these_cameras = {k: v for k, v in controller.cameras.items() if v.video_writer is not None}
        else:
            these_cameras = controller.cameras
        cameras.update(these_cameras)
    return cameras


ISearchable = Union[pydantic.BaseModel, Dict, List]
_ISearchableTypeChecker = tuple(get_args(ISearchable))  # pre-compute for performance


def get_fields_of_type(
    searchable: ISearchable, target_type: Type[T], /, is_recursive: bool = True, stop_recursion_on_type: bool = True
) -> List[T]:
    """_summary_

    Args:
        searchable (ISearchable): A searchable object.
        target_type (Type[T]): Target type to search for.
        is_recursive (bool, optional): Whether to perform a recursive search. Defaults to True.
        stop_recursion_on_type (bool, optional): Whether to stop recursive search when a target type is found. Defaults to True.

    Raises:
        ValueError: Unsupported model type.

    Returns:
        List[T]: A list with all objects of the target type
    """
    result: list[T] = []

    _iterable: Iterable[Any]
    _is_type: bool

    if isinstance(searchable, dict):
        _iterable = list(searchable.values())
    elif isinstance(searchable, list):
        _iterable = searchable
    elif isinstance(searchable, pydantic.BaseModel):
        _iterable = [getattr(searchable, field) for field in searchable.model_fields.keys()]
    else:
        raise ValueError(f"Unsupported model type: {type(searchable)}")

    for field in _iterable:
        _is_type = False
        if isinstance(field, target_type):
            result.append(field)
            _is_type = True
        if is_recursive and isinstance(field, _ISearchableTypeChecker) and not (stop_recursion_on_type and _is_type):
            result.extend(get_fields_of_type(field, target_type, is_recursive))
    return result
