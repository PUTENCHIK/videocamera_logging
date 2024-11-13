from typing import Annotated
from pprint import pprint
from datetime import datetime

from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder

from src import Config
from src.database import DBSession, get_db_session
from src.cameras import CameraAdd
from src.cameras.logic import _add_camera, _get_cameras


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
async def add_camera(camera: Annotated[CameraAdd, Form()], db: DBSession = Depends(get_db_session)):
    new_camera = _add_camera(camera, db)

    return RedirectResponse(f"{router_path}", status_code=302)
