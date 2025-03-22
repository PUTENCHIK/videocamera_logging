from pydantic import BaseModel


class CameraAddOrEdit(BaseModel):
    address: str
