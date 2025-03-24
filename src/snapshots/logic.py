from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session

from src import Config
from src.snapshots import (
    TrackableClassAdd, TrackableClassModel, SnapshotAdd, SnapshotModel, ObjectAdd, ObjectModel,
    Bbox)
from src.detecting import DetectingResults


def _add_trackable_class(class_: TrackableClassAdd, db: Session) -> Optional[TrackableClassModel]:
    new_class = TrackableClassModel(
        name=class_.name
    )

    db.add(new_class)
    db.commit()
    db.refresh(new_class)

    return new_class


def _get_trackable_class(name: str, db: Session) -> Optional[TrackableClassModel]:
    return db.query(TrackableClassModel).filter_by(name=name).first()


async def add_trackable_classes(db: Session):
    for label, name in Config.detecting_classes_names.items():
        class_ = _get_trackable_class(name, db)
        if class_ is None:
            scheme = TrackableClassAdd(name=name)
            _add_trackable_class(scheme, db)


def _add_snapshot(snapshot: SnapshotAdd, db: Session) -> Optional[SnapshotModel]:
    new_snapshot = SnapshotModel(
        camera_id=snapshot.camera_id,
        detecting_time=snapshot.detecting_time,
        created_at=datetime.now()
    )

    db.add(new_snapshot)
    db.commit()
    db.refresh(new_snapshot)

    return new_snapshot


def _add_object(object: ObjectModel, db: Session) -> Optional[ObjectModel]:
    new_object = ObjectModel(
        snapshot_id=object.snapshot_id,
        class_id=object.class_id,
        bbox=object.bbox.dict(),
        created_at=datetime.now()
    )

    db.add(new_object)
    db.commit()
    db.refresh(new_object)

    return new_object


def _parse_detecting_results(results: DetectingResults, camera_id: int, db: Session) -> SnapshotModel:
    snapshot_scheme = SnapshotAdd(
        camera_id=camera_id,
        detecting_time=results.time
    )
    new_snapshot = _add_snapshot(snapshot_scheme, db)
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
        _add_object(object_scheme, db)
    
    return new_snapshot
