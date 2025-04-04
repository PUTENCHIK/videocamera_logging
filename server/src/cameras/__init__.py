from .schemes import Camera, CameraAddOrEdit, CameraAfterEdit
from .models import Camera as CameraModel

from .logic import (
    _add_camera,
    _get_cameras,
    _get_monitoring_cameras,
    _get_camera,
    _edit_camera,
    _delete_camera,
    _switch_camera
)