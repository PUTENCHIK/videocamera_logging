from sqlalchemy import Column, Integer, Float, String, DateTime, JSON
from src.database import BaseDBModel


class Snapshot(BaseDBModel):
    __tablename__ = "snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    camera_id = Column(Integer, nullable=False, unique=False)
    detecting_time = Column(Float, nullable=False, unique=False)
    created_at = Column(DateTime, nullable=False, unique=False)
    deleted_at = Column(DateTime, nullable=True, unique=False)


class Object(BaseDBModel):
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    snapshot_id = Column(Integer, nullable=False, unique=False)
    class_id = Column(Integer, nullable=False, unique=False)
    bbox = Column(JSON, nullable=False)
    created_at = Column(DateTime, nullable=False, unique=False)
    deleted_at = Column(DateTime, nullable=True, unique=False)


class TrackableClass(BaseDBModel):
    __tablename__ = "trackable_classes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
