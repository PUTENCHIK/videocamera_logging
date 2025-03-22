from datetime import datetime
from pydantic import BaseModel


class Camera(BaseModel):
    id: int
    address: str
    is_monitoring: bool
    created_at: datetime
    deleted_at: datetime | None
