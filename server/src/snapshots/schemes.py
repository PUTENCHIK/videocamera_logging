from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

from src.classes import TrackableClass


class Bbox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float

    class Config:
        from_attributes = True


class ObjectAdd(BaseModel):
    snapshot_id: int
    label: int
    probability: float
    bbox: Bbox
    created_at: datetime

    class Config:
        from_attributes = True


class Object(ObjectAdd):
    id: int
    created_at: datetime
    deleted_at: Optional[datetime] = None


class ObjectFull(BaseModel):
    id: int
    snapshot_id: int
    label: int
    trackable_class: Optional[TrackableClass] = None
    probability: float
    bbox: Bbox
    created_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SnapshotAdd(BaseModel):
    camera_id: int
    detecting_time: float
    created_at: datetime

    class Config:
        from_attributes = True


class Snapshot(SnapshotAdd):
    id: int
    created_at: datetime
    deleted_at: Optional[datetime] = None


class SnapshotFull(BaseModel):
    id: int
    camera_id: int
    detecting_time: float
    objects: List[ObjectFull]
    created_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ObjectFullWithSnapshot(ObjectFull):
    snapshot: Snapshot
