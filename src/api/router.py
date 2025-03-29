from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import Config
from src.database import get_db_session
from src.cameras import Camera, _get_camera, _get_cameras
from src.snapshots import SnapshotFull, _get_snapshots
from src.classes import TrackableClassFull, _get_classes


api_router = APIRouter(prefix=f"/{Config.routers.api_name}",
                       tags=[Config.routers.api_name])


@api_router.get("/cameras", response_model=List[Camera])
async def get_cameras(db: AsyncSession = Depends(get_db_session)):
    cameras = await _get_cameras(db)
    return cameras


@api_router.get("/cameras/{camera_id}", response_model=Optional[Camera])
async def get_camera(camera_id: int,
                     db: AsyncSession = Depends(get_db_session)):
    camera = await _get_camera(camera_id, db)

    return camera


@api_router.get("/snapshots", response_model=List[SnapshotFull])
async def get_snapshots(db: AsyncSession = Depends(get_db_session)):
    snapshots = await _get_snapshots(db)
    return snapshots


@api_router.get("/classes", response_model=List[TrackableClassFull])
async def get_classes(db: AsyncSession = Depends(get_db_session)):
    classes = await _get_classes(db)
    return classes
