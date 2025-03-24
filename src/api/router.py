from typing import Optional, List

from fastapi import APIRouter, Depends

from src.database import DBSession, get_db_session
from src.cameras import Camera, _get_camera, _get_cameras
from src.snapshots import SnapshotFull, _get_snapshots


api_router = APIRouter()
router_path = "/api"


@api_router.get(f"{router_path}/cameras", response_model=List[Camera])
async def get_cameras(db: DBSession = Depends(get_db_session)):
    cameras = _get_cameras(db)
    return cameras


@api_router.get(router_path + "/cameras/{camera_id}", response_model=Optional[Camera])
async def get_camera(camera_id: int, db: DBSession = Depends(get_db_session)):
    camera = _get_camera(camera_id, db)

    return camera


@api_router.get(f"{router_path}/snapshots", response_model=List[SnapshotFull])
async def get_snapshots(db: DBSession = Depends(get_db_session)):
    snapshots = _get_snapshots(db)
    return snapshots
