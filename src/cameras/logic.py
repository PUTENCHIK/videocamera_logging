from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from src.cameras import CameraModel, CameraAddOrEdit, Camera


def _add_camera(camera: CameraAddOrEdit, db: Session) -> Optional[CameraModel]:
    new_camera = CameraModel(
        login=camera.login,
        ip=camera.ip,
        password=camera.password,
        port=camera.port,
        created_at=datetime.now(),
        deleted_at=None
    )

    db.add(new_camera)
    db.commit()
    db.refresh(new_camera)

    return new_camera


def _get_cameras(db: Session):
    return db.query(CameraModel).filter_by(deleted_at=None).all()


def _get_camera(id: int, db: Session):
    return db.query(CameraModel).filter_by(id=id, deleted_at=None).first()


def _edit_camera(camera: CameraModel, fields: CameraAddOrEdit, db: Session) -> CameraModel:
    camera.login = fields.login
    camera.password = fields.password
    camera.ip = fields.ip
    camera.port = fields.port

    db.commit()

    return camera
