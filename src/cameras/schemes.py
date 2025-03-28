from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class Camera(BaseModel):
    id: int
    address: str
    is_monitoring: bool
    created_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CameraAddOrEdit(BaseModel):
    address: str


class CameraAfterEdit(BaseModel):
    success: bool = False
    camera: Optional[Camera] = None
