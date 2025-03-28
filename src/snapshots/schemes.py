from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

from src.classes import TrackableClass


class Snapshot(BaseModel):
    id: int
    camera_id: int
    detecting_time: float
    created_at: datetime
    deleted_at: Optional[datetime] = None


class Bbox(BaseModel):
    probability: float
    x1: int
    y1: int
    x2: int
    y2: int


class Object(BaseModel):
    id: int
    snapshot_id: int
    bbox: Bbox
    created_at: datetime
    deleted_at: Optional[datetime] = None


class SnapshotAdd(BaseModel):
    camera_id: int
    detecting_time: float


class ObjectAdd(BaseModel):
    snapshot_id: int
    class_id: int
    bbox: Bbox


class ObjectFull(Object):
    trackable_class: TrackableClass


class SnapshotFull(Snapshot):
    objects: List[ObjectFull]
