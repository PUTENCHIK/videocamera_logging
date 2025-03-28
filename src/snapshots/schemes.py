from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

from src.classes import TrackableClass


class Bbox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float


class ObjectAdd(BaseModel):
    snapshot_id: int
    label: int
    probability: float
    bbox: Bbox


class ObjectFull(BaseModel):
    id: int
    snapshot_id: int
    trackable_class: Optional[TrackableClass] = None
    probability: float
    bbox: Bbox
    created_at: datetime
    deleted_at: Optional[datetime] = None


class SnapshotAdd(BaseModel):
    camera_id: int
    detecting_time: float


class SnapshotFull(BaseModel):
    id: int
    camera_id: int
    detecting_time: float
    objects: List[ObjectFull]
    created_at: datetime
    deleted_at: Optional[datetime] = None
