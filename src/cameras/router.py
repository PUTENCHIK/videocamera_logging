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
async def index(request: Request, db: DBSession = Depends(get_db_session)):
    cameras = _get_cameras(db)
    json_cameras = jsonable_encoder(cameras)
    for i, camera in enumerate(json_cameras):
        d = datetime.strptime(camera['created_at'], "%Y-%m-%dT%H:%M:%S.%f")
        camera['created_at'] = d.strftime("%d.%m.%Y %H:%M:%S")
        json_cameras[i] = camera

    return Config.templates.TemplateResponse(
        request=request,
        name="cameras.html",
        context={"cameras": json_cameras}
    )


@cameras_router.post(f"{router_path}/add", response_class=RedirectResponse)
async def add_camera(camera: Annotated[CameraAddOrEdit, Form()], db: DBSession = Depends(get_db_session)):
    new_camera = _add_camera(camera, db)

    return RedirectResponse(f"{router_path}", status_code=302)


@cameras_router.get(router_path + "/{camera_id}", response_model=Camera)
async def get_camera(camera_id: int, db: DBSession = Depends(get_db_session)):
    camera = _get_camera(camera_id, db)

    return camera


@cameras_router.post(router_path + "/{camera_id}/edit", response_class=RedirectResponse)
async def edit_camera(camera_id: int, camera: Annotated[CameraAddOrEdit, Form()], db: DBSession = Depends(get_db_session)):
    db_camera = _get_camera(camera_id, db)

    if db_camera is not None:
        _edit_camera(db_camera, camera, db)
    
    return RedirectResponse(f"{router_path}", status_code=302)


@cameras_router.post(router_path + "/{camera_id}/delete", response_class=RedirectResponse)
async def delete_camera(camera_id: int, db: DBSession = Depends(get_db_session)):
    db_camera = _get_camera(camera_id, db)

    if db_camera is not None:
        _delete_camera(db_camera, db)
    
    return RedirectResponse(f"{router_path}", status_code=302)
