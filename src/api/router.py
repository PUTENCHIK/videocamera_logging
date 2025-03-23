from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from src import Config
from src.database import DBSession, get_db_session
from src.cameras import Camera, _get_camera, _get_cameras


api_router = APIRouter()
router_path = "/api"


@api_router.get(f"{router_path}/cameras", response_class=JSONResponse)
async def get_cameras(request: Request, db: DBSession = Depends(get_db_session)):
    cameras = _get_cameras(db)
    json_cameras = jsonable_encoder(cameras)

    return JSONResponse(content=json_cameras)


@api_router.get(router_path + "/cameras/{camera_id}", response_model=Camera)
async def get_camera(camera_id: int, db: DBSession = Depends(get_db_session)):
    camera = _get_camera(camera_id, db)

    return camera
