from pydantic import BaseModel


class CameraAdd(BaseModel):
    login: str
    ip: str | None
    password: str
    port: int
