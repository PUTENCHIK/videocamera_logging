from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from src.cameras import CameraModel, CameraAdd, Camera


def _add_camera(camera: CameraAdd, db: Session) -> Optional[CameraModel]:
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


def _get_cameras(db: Session):# -> list[Camera]:
    return db.query(CameraModel).filter_by(deleted_at=None).all()
