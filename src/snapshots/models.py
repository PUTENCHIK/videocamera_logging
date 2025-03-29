from sqlalchemy import Column, Integer, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship

from src.database import BaseDBModel
from src.classes import TrackableClass


class Snapshot(BaseDBModel):
    __tablename__ = "snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    camera_id = Column(Integer, ForeignKey("cameras.id"), nullable=False)
    detecting_time = Column(Float, nullable=False, unique=False)
    created_at = Column(DateTime, nullable=False, unique=False)
    deleted_at = Column(DateTime, nullable=True, unique=False, default=None)

    camera = relationship("Camera", back_populates="snapshots")
    objects = relationship("Object", back_populates="snapshot")


class Object(BaseDBModel):
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    snapshot_id = Column(Integer, ForeignKey("snapshots.id"), nullable=False)
    label = Column(Integer, ForeignKey("trackable_classes.label"), nullable=False)
    probability = Column(Float, nullable=False, unique=False)
    bbox = Column(JSON, nullable=False, unique=False)
    created_at = Column(DateTime, nullable=False, unique=False)
    deleted_at = Column(DateTime, nullable=True, unique=False, default=None)

    snapshot = relationship("Snapshot", back_populates="objects")
    trackable_class = relationship("TrackableClass", back_populates="objects")
