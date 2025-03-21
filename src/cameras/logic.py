from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from src.cameras import CameraModel, CameraAddOrEdit, Camera


def _add_camera(camera: CameraAddOrEdit, db: Session) -> Optional[CameraModel]:
    new_camera = CameraModel(
        address=camera.address,
        created_at=datetime.now(),
        deleted_at=None
    )

    db.add(new_camera)
    db.commit()
    db.refresh(new_camera)

    return new_camera


def _get_cameras(db: Session):
    return db.query(CameraModel).filter_by(deleted_at=None).all()


def _get_camera(id: int, db: Session) -> CameraModel:
    return db.query(CameraModel).filter_by(id=id, deleted_at=None).first()


def _edit_camera(camera: CameraModel, fields: CameraAddOrEdit, db: Session) -> CameraModel:
    camera.address = fields.address
    db.commit()

    return camera


def _delete_camera(camera: CameraModel, db: Session) -> CameraModel:
    camera.deleted_at = datetime.now()
    db.commit()

    return camera
