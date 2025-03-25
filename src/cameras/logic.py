from typing import Optional, List
from datetime import datetime
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.cameras import CameraModel, CameraAddOrEdit


async def _add_camera(camera: CameraAddOrEdit, db: AsyncSession) -> CameraModel:
    query = insert(CameraModel) \
        .values(address=camera.address, created_at=datetime.now()) \
        .returning(CameraModel)
    result = await db.execute(query)
    new_camera = result.scalar_one()

    await db.commit()
    await db.refresh(new_camera)

    return new_camera


async def _get_cameras(db: AsyncSession) -> List[CameraModel]:
    query = select(CameraModel).where(CameraModel.deleted_at == None)
    result = await db.execute(query)
    return result.scalars().all()


async def _get_monitoring_cameras(db: AsyncSession) -> List[CameraModel]:
    query = select(CameraModel).where(CameraModel.deleted_at == None, CameraModel.is_monitoring)
    result = await db.execute(query)
    return result.scalars().all()


async def _get_camera(id: int, db: AsyncSession) -> Optional[CameraModel]:
    query = select(CameraModel).where(CameraModel.deleted_at == None, CameraModel.id == id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def _edit_camera(camera: CameraModel, fields: CameraAddOrEdit, db: AsyncSession) -> CameraModel:
    query = update(CameraModel) \
        .where(CameraModel.id == camera.id) \
        .values(address=fields.address) \
        .returning(CameraModel)
    result = await db.execute(query)
    updated_camera = result.scalar_one()

    await db.commit()
    await db.refresh(updated_camera)

    return updated_camera


async def _delete_camera(camera: CameraModel, db: AsyncSession) -> CameraModel:
    query = update(CameraModel) \
        .where(CameraModel.id == camera.id) \
        .values(deleted_at=datetime.now()) \
        .returning(CameraModel)
    result = await db.execute(query)
    deleted_camera = result.scalar_one()

    await db.commit()
    await db.refresh(deleted_camera)

    return deleted_camera


async def _switch_camera(camera: CameraModel, db: AsyncSession) -> CameraModel:
    query = update(CameraModel) \
        .where(CameraModel.id == camera.id) \
        .values(is_monitoring=not camera.is_monitoring) \
        .returning(CameraModel)
    result = await db.execute(query)
    switched_camera = result.scalar_one()

    await db.commit()
    await db.refresh(switched_camera)

    return switched_camera
