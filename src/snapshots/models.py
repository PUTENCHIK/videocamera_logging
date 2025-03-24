from sqlalchemy import Column, Integer, Float, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship

from src.database import BaseDBModel


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
    class_id = Column(Integer, ForeignKey("trackable_classes.id"), nullable=False)
    bbox = Column(JSON, nullable=False)
    created_at = Column(DateTime, nullable=False, unique=False)
    deleted_at = Column(DateTime, nullable=True, unique=False, default=None)

    snapshot = relationship("Snapshot", back_populates="objects")
    trackable_class = relationship("TrackableClass", back_populates="objects")


class TrackableClass(BaseDBModel):
    __tablename__ = "trackable_classes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    objects = relationship("Object", back_populates="trackable_class")
