from typing import Optional, List
from datetime import datetime
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.cameras import CameraModel, CameraAddOrEdit, Camera


async def _add_camera(fields: CameraAddOrEdit,
                      db: AsyncSession) -> Camera:
    query = (insert(CameraModel)
        .values(address=fields.address,
                created_at=datetime.now())
        .returning(CameraModel))
    result = await db.execute(query)
    new_camera = result.scalar_one()

    await db.commit()
    await db.refresh(new_camera)

    return Camera.model_validate(new_camera)


async def _get_cameras(db: AsyncSession) -> List[Camera]:
    query = select(CameraModel).where(CameraModel.deleted_at == None)
    result = await db.execute(query)
    return [Camera.model_validate(camera)
            for camera in result.scalars().all()]


async def _get_monitoring_cameras(db: AsyncSession) -> List[Camera]:
    query = (select(CameraModel)
        .where(CameraModel.deleted_at == None,
               CameraModel.is_monitoring))
    result = await db.execute(query)
    return [Camera.model_validate(camera)
            for camera in result.scalars().all()]


async def _get_camera(id: int,
                      db: AsyncSession) -> Optional[Camera]:
    query = (select(CameraModel)
        .where(CameraModel.deleted_at == None,
               CameraModel.id == id))
    result = await db.execute(query)
    camera = result.scalar_one_or_none()
    return Camera.model_validate(camera) if camera is not None else None


async def _edit_camera(id: int,
                       fields: CameraAddOrEdit,
                       db: AsyncSession) -> Camera:
    query = (update(CameraModel)
        .where(CameraModel.id == id)
        .values(address=fields.address)
        .returning(CameraModel))
    result = await db.execute(query)
    updated_camera = result.scalar_one()

    await db.commit()
    await db.refresh(updated_camera)

    return Camera.model_validate(updated_camera)


async def _delete_camera(id: int,
                         db: AsyncSession) -> Camera:
    query = (update(CameraModel)
        .where(CameraModel.id == id)
        .values(deleted_at=datetime.now())
        .returning(CameraModel))
    result = await db.execute(query)
    deleted_camera = result.scalar_one()

    await db.commit()
    await db.refresh(deleted_camera)

    return Camera.model_validate(deleted_camera)


async def _switch_camera(id: int,
                         is_monitoring: bool,
                         db: AsyncSession) -> Camera:
    query = (update(CameraModel)
        .where(CameraModel.id == id)
        .values(is_monitoring=not is_monitoring)
        .returning(CameraModel))
    result = await db.execute(query)
    switched_camera = result.scalar_one()

    await db.commit()
    await db.refresh(switched_camera)

    return Camera.model_validate(switched_camera)


async def _restore_camera(id: int,
                          db: AsyncSession) -> Optional[Camera]:
    query = (update(CameraModel)
        .where(CameraModel.id == id)
        .values(deleted_at=None,
                is_monitoring=False)
        .returning(CameraModel))
    result = await db.execute(query)
    camera = result.scalar_one_or_none()

    await db.commit()
    if camera is not None:
        await db.refresh(camera)

    return Camera.model_validate(camera) if camera is not None else None
