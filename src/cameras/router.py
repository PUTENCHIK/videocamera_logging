from typing import Annotated
from pprint import pprint
from datetime import datetime

from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder

from src import Config
from src.database import DBSession, get_db_session
from src.cameras import CameraAddOrEdit, Camera
from src.cameras.logic import _add_camera, _get_cameras, _get_camera, _edit_camera, _delete_camera


cameras_router = APIRouter()
router_path = "/cameras"


@cameras_router.get(f"{router_path}", response_class=HTMLResponse)
async def index(request: Request):
    return Config.templates.TemplateResponse(
        request=request,
        name="cameras.html"
    )


@cameras_router.post(f"{router_path}/add", response_class=JSONResponse)
async def add_camera(camera: CameraAddOrEdit, db: DBSession = Depends(get_db_session)):
    new_camera = _add_camera(camera, db)
    json_new_camera = jsonable_encoder(new_camera)
    return JSONResponse(content=json_new_camera)


@cameras_router.get(router_path + "/{camera_id}", response_model=Camera)
async def get_camera(camera_id: int, db: DBSession = Depends(get_db_session)):
    camera = _get_camera(camera_id, db)

    return camera


@cameras_router.patch(router_path + "/{camera_id}/edit", response_class=JSONResponse)
async def edit_camera(camera_id: int, camera: CameraAddOrEdit, db: DBSession = Depends(get_db_session)):
    db_camera = _get_camera(camera_id, db)

    result = {"success": False}
    if db_camera is not None:
        _edit_camera(db_camera, camera, db)
        result["success"] = True
        result["camera"] = jsonable_encoder(_get_camera(camera_id, db))
    
    return JSONResponse(content=result)


@cameras_router.delete(router_path + "/{camera_id}/delete", response_class=JSONResponse)
async def delete_camera(camera_id: int, db: DBSession = Depends(get_db_session)):
    db_camera = _get_camera(camera_id, db)

    result = {"success": False}
    if db_camera is not None:
        _delete_camera(db_camera, db)
        result["success"] = True
    
    return JSONResponse(content=result)
