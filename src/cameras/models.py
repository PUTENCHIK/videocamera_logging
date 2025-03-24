from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.database import BaseDBModel


class Camera(BaseDBModel):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String, nullable=False, unique=False)
    is_monitoring = Column(Boolean, nullable=False, default=False, unique=False)
    created_at = Column(DateTime, nullable=False, unique=False)
    deleted_at = Column(DateTime, nullable=True, unique=False, default=None)

    snapshots = relationship("Snapshot", back_populates="camera")
