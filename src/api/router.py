from typing import Optional, List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src import Config
from src.database import get_db_session
from src.cameras import Camera, _get_camera, _get_cameras
from src.snapshots import SnapshotFull, _get_snapshots


api_router = APIRouter()
router_path = "/api"


@api_router.get(f"{router_path}/cameras", response_model=List[Camera])
async def get_cameras(db: AsyncSession = Depends(get_db_session)):
    cameras = await _get_cameras(db)
    return cameras


@api_router.get(router_path + "/cameras/{camera_id}", response_model=Optional[Camera])
async def get_camera(camera_id: int, db: AsyncSession = Depends(get_db_session)):
    camera = await _get_camera(camera_id, db)

    return camera


@api_router.get(f"{router_path}/snapshots", response_model=List[SnapshotFull])
async def get_snapshots(db: AsyncSession = Depends(get_db_session)):
    snapshots = await _get_snapshots(db)
    return snapshots


@api_router.get(f"{router_path}/class_colors", response_class=JSONResponse)
async def get_trackable_class_colors():
    return Config.detecting_classes_colors
