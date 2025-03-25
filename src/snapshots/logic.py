from typing import Optional, List
from datetime import datetime
from sqlalchemy import select, insert, desc
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src import Config
from src.snapshots import (
    TrackableClassAdd, TrackableClassModel, SnapshotAdd, SnapshotModel, ObjectAdd, ObjectModel, Bbox)
from src.detecting import DetectingResults


async def _add_trackable_class(class_: TrackableClassAdd, db: AsyncSession) -> Optional[TrackableClassModel]:
    query = insert(TrackableClassModel).values(
        name=class_.name
    ).returning(TrackableClassModel)
    result = await db.execute(query)
    new_class = result.scalar_one()
    
    await db.commit()
    await db.refresh(new_class)

    return new_class


async def _get_trackable_class(name: str, db: AsyncSession) -> Optional[TrackableClassModel]:
    query = select(TrackableClassModel).where(TrackableClassModel.name == name)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def add_trackable_classes(db: AsyncSession):
    for _, name in Config.detecting_classes_names.items():
        class_ = await _get_trackable_class(name, db)
        if class_ is None:
            scheme = TrackableClassAdd(name=name)
            await _add_trackable_class(scheme, db)


async def _add_snapshot(snapshot: SnapshotAdd, db: AsyncSession) -> SnapshotModel:
    query = insert(SnapshotModel) \
        .values(
            camera_id=snapshot.camera_id,
            detecting_time=snapshot.detecting_time,
            created_at=datetime.now()) \
        .returning(SnapshotModel)
    result = await db.execute(query)
    new_snapshot = result.scalar_one()

    await db.commit()
    await db.refresh(new_snapshot)

    return new_snapshot


async def _add_object(object: ObjectModel, db: AsyncSession) -> Optional[ObjectModel]:
    query = insert(ObjectModel) \
        .values(
            snapshot_id=object.snapshot_id,
            class_id=object.class_id,
            bbox=object.bbox.dict(),
            created_at=datetime.now()) \
        .returning(ObjectModel)
    result = await db.execute(query)
    new_object = result.scalar_one()

    await db.commit()
    await db.refresh(new_object)

    return new_object


async def _parse_detecting_results(results: DetectingResults, camera_id: int, db: AsyncSession) -> SnapshotModel:
    snapshot_scheme = SnapshotAdd(
        camera_id=camera_id,
        detecting_time=results.time
    )
    new_snapshot = await _add_snapshot(snapshot_scheme, db)
    results_json = results.to_json()
    for object in results_json["objects"]:
        x1, y1, x2, y2 = object["box"]
        bbox = Bbox(
            probability=object["prob"],
            x1=x1, y1=y1,
            x2=x2, y2=y2,
        )
        object_scheme = ObjectAdd(
            snapshot_id=new_snapshot.id,
            class_id=object["class_index"]+1,
            bbox=bbox
        )
        await _add_object(object_scheme, db)
    
    return new_snapshot


async def _get_snapshots(db: AsyncSession) -> List[SnapshotModel]:
    query = select(SnapshotModel) \
        .options(joinedload(SnapshotModel.objects) \
        .options(joinedload(ObjectModel.trackable_class))) \
        .where(SnapshotModel.deleted_at == None) \
        .order_by(desc(SnapshotModel.created_at))
    result = await db.execute(query)
    return result.scalars().unique().all()
