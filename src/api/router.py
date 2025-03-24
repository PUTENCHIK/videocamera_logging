from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from src.database import DBSession, get_db_session
from src.cameras import Camera, _get_camera, _get_cameras
from src.snapshots import Snapshot, _get_snapshots


api_router = APIRouter()
router_path = "/api"


@api_router.get(f"{router_path}/cameras", response_class=JSONResponse)
async def get_cameras(db: DBSession = Depends(get_db_session)):
    cameras = _get_cameras(db)
    json_cameras = jsonable_encoder(cameras)

    return JSONResponse(content=json_cameras)


@api_router.get(router_path + "/cameras/{camera_id}", response_model=Optional[Camera])
async def get_camera(camera_id: int, db: DBSession = Depends(get_db_session)):
    camera = _get_camera(camera_id, db)

    return camera if camera is not None else None


@api_router.get(f"{router_path}/snapshots", response_class=JSONResponse)
async def get_snapshots(db: DBSession = Depends(get_db_session)):
    snapshots = _get_snapshots(db)
    for snapshot in snapshots:
        snapshot.objects
    json_snapshots = jsonable_encoder(snapshots)

    return JSONResponse(content=json_snapshots)
