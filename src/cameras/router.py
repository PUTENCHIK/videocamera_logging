from typing import Optional
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from src import Config
from src.database import DBSession, get_db_session
from src.cameras import (CameraAddOrEdit, Camera, CameraAfterEdit,
                         _add_camera, _get_camera, _edit_camera,
                         _delete_camera, _switch_camera)


cameras_router = APIRouter()
router_path = "/cameras"


@cameras_router.get(f"{router_path}", response_class=HTMLResponse)
async def index(request: Request):
    return Config.templates.TemplateResponse(
        request=request,
        name="cameras.html"
    )


@cameras_router.post(f"{router_path}/add", response_model=Optional[Camera])
async def add_camera(camera: CameraAddOrEdit, db: DBSession = Depends(get_db_session)):
    new_camera = _add_camera(camera, db)
    return new_camera


@cameras_router.patch(router_path + "/{camera_id}/edit", response_model=CameraAfterEdit)
async def edit_camera(camera_id: int, camera: CameraAddOrEdit, db: DBSession = Depends(get_db_session)):
    db_camera = _get_camera(camera_id, db)

    result = CameraAfterEdit()
    if db_camera is not None:
        edited_camera = _edit_camera(db_camera, camera, db)
        result.success = True
        result.camera = edited_camera
    
    return result


@cameras_router.delete(router_path + "/{camera_id}/delete", response_model=CameraAfterEdit)
async def delete_camera(camera_id: int, db: DBSession = Depends(get_db_session)):
    db_camera = _get_camera(camera_id, db)

    result = CameraAfterEdit()
    if db_camera is not None:
        _delete_camera(db_camera, db)
        result.success = True
    
    return result


@cameras_router.patch(router_path + "/{camera_id}/switch", response_model=CameraAfterEdit)
async def switch_camera(camera_id: int, db: DBSession = Depends(get_db_session)):
    db_camera = _get_camera(camera_id, db)

    result = CameraAfterEdit()
    if db_camera is not None:
        switched_camera = _switch_camera(db_camera, db)
        result.success = True
        result.camera = switched_camera
    
    return result
