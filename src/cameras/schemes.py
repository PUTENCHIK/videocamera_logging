from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class Camera(BaseModel):
    id: int
    address: str
    is_monitoring: bool
    created_at: datetime
    deleted_at: Optional[datetime] = None


class CameraAddOrEdit(BaseModel):
    address: str


class CameraAfterEdit(BaseModel):
    success: bool = False
    camera: Optional[Camera] = None
