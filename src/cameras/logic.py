from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session

from src.cameras import CameraModel, CameraAddOrEdit


def _add_camera(camera: CameraAddOrEdit, db: Session) -> Optional[CameraModel]:
    new_camera = CameraModel(
        address=camera.address,
        created_at=datetime.now()
    )

    db.add(new_camera)
    db.commit()
    db.refresh(new_camera)

    return new_camera


def _get_cameras(db: Session):
    return db.query(CameraModel).filter_by(deleted_at=None).all()


def _get_monitoring_cameras(db: Session):
    return db.query(CameraModel).filter_by(is_monitoring=True,
                                           deleted_at=None).all()


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


def _switch_camera(camera: CameraModel, db: Session) -> CameraModel:
    camera.is_monitoring = not camera.is_monitoring
    db.commit()

    return camera
