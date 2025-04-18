from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class Color(BaseModel):
    r: int
    g: int
    b: int


class TrackableClassAddOrEdit(BaseModel):
    name: str
    label: str
    title: str
    color: str


class TrackableClass(BaseModel):
    id: int
    name: str
    label: int
    title: str
    color: Color

    class Config:
        from_attributes = True

class TrackableClassFull(TrackableClass):
    created_at: datetime
    deleted_at: Optional[datetime] = None


class TrackableClassAfterEdit(BaseModel):
    success: bool = False
    class_: Optional[TrackableClassFull] = None
    error: Optional[str] = None

    class Config:
        from_attributes = True
