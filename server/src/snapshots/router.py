from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import Config
from src.database import get_db_session
from src.snapshots import (_get_snapshots, _get_objects,
                           SnapshotFull, ObjectFullWithSnapshot)


snapshots_router = APIRouter(prefix=f"/{Config.routers.snapshots_name}",
                             tags=[Config.routers.snapshots_name])


@snapshots_router.get("", response_model=List[SnapshotFull])
async def get_snapshots(db: AsyncSession = Depends(get_db_session)):
    snapshots = await _get_snapshots(db)
    return snapshots


@snapshots_router.get("/objects", response_model=List[ObjectFullWithSnapshot])
async def get_objects(db: AsyncSession = Depends(get_db_session)):
    objects = await _get_objects(db)
    return objects
