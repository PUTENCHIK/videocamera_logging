from typing import Optional, List
from datetime import datetime
from sqlalchemy import select, insert, desc
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.snapshots import (SnapshotAdd, SnapshotModel, ObjectModel,
                           ObjectAdd, Snapshot, Object,
                           SnapshotFull, ObjectFullWithSnapshot)


async def _add_snapshot(fields: SnapshotAdd,
                        db: AsyncSession) -> Snapshot:
    query = (insert(SnapshotModel)
        .values(
            camera_id=fields.camera_id,
            detecting_time=fields.detecting_time,
            created_at=datetime.now())
        .returning(SnapshotModel))
    result = await db.execute(query)
    new_snapshot = result.scalar_one()

    await db.commit()
    await db.refresh(new_snapshot)

    return Snapshot.model_validate(new_snapshot)


async def _add_object(fields: ObjectAdd,
                      db: AsyncSession) -> Object:
    query = (insert(ObjectModel)
        .values(
            snapshot_id=fields.snapshot_id,
            label=fields.label,
            probability=fields.probability,
            bbox=fields.bbox.model_dump(),
            created_at=datetime.now())
        .returning(ObjectModel))
    result = await db.execute(query)
    new_object = result.scalar_one()

    await db.commit()
    await db.refresh(new_object)

    return Object.model_validate(new_object)


async def _get_snapshots(db: AsyncSession) -> List[SnapshotFull]:
    query = (select(SnapshotModel)
        .options(joinedload(SnapshotModel.objects)
        .options(joinedload(ObjectModel.trackable_class)))
        .where(SnapshotModel.deleted_at == None)
        .order_by(desc(SnapshotModel.created_at)))
    result = await db.execute(query)
    snapshots = result.scalars().unique().all()
    return [SnapshotFull.model_validate(snapshot)
            for snapshot in snapshots]


async def _get_objects(db: AsyncSession) -> List[ObjectFullWithSnapshot]:
    query = (select(ObjectModel)
        .options(joinedload(ObjectModel.trackable_class))
        .options(joinedload(ObjectModel.snapshot))
        .where(ObjectModel.deleted_at == None))
    result = await db.execute(query)
    objects = result.scalars().unique().all()
    return [ObjectFullWithSnapshot.model_validate(object)
            for object in objects]
