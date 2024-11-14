from pydantic import BaseModel


class CameraAddOrEdit(BaseModel):
    login: str
    ip: str | None
    password: str
    port: int
