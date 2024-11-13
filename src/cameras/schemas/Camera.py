from datetime import datetime
from pydantic import BaseModel


class Camera(BaseModel):
    id: int
    login: str
    ip: str | None
    password: str
    port: int
    created_at: datetime
    deleted_at: datetime
