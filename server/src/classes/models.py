from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship

from src.database import BaseDBModel


class TrackableClass(BaseDBModel):
    __tablename__ = "trackable_classes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    label = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    color = Column(JSON, nullable=False)
    created_at = Column(DateTime, nullable=False, unique=False)
    deleted_at = Column(DateTime, nullable=True, unique=False, default=None)

    objects = relationship(
        "Object",
        back_populates="trackable_class",
        primaryjoin="and_(Object.label == TrackableClass.label, TrackableClass.deleted_at == None)"
    )
