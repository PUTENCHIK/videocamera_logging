from pathlib import Path
from fastapi.templating import Jinja2Templates

from src.database import DBSession
from src.snapshots import (
    TrackableClassAdd, _get_trackable_class, _add_trackable_class)


class Config:
    app_name = "src.app:app"
    app_host = "localhost"
    app_port = 5050
    app_icon = Path("favicon.ico")

    templates = Jinja2Templates(directory="static/html")

    model_storage = Path("storage/models")
    model_name = "yolo11l_100.pt"
    model_confidence = 0.75
    detecting_classes_names = {
        0: 'human',
        1: 'bear',
        2: 'elk',
        3: 'fox',
    }
    # BGR encoding
    detecting_classes_colors = {
        0: (53, 124, 240),
        1: (52, 235, 161),
        2: (252, 50, 192),
        3: (235, 212, 38),
    }
    detecting_delay = 1 #sec

    @staticmethod
    async def add_trackable_classes():
        db = DBSession()
        try:
            for label, name in Config.detecting_classes_names.items():
                class_ = _get_trackable_class(name, db)
                if class_ is None:
                    scheme = TrackableClassAdd(name=name)
                    _add_trackable_class(scheme, db)
        finally:
            db.close()
