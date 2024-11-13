from sqlalchemy import Column, Integer, String, DateTime

from src.database import BaseDBModel


class Camera(BaseDBModel):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, nullable=False, unique=False)
    ip = Column(String, nullable=True, unique=False)
    password = Column(String, nullable=False, unique=False)
    port = Column(Integer, nullable=False, unique=False)
    created_at = Column(DateTime, nullable=False, unique=False)
    deleted_at = Column(DateTime, nullable=True, unique=False)
