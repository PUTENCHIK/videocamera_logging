from pathlib import Path
from fastapi.templating import Jinja2Templates


class ConfigApp:
    name = "src.app:app"
    host = "localhost"
    port = 5050
    port_vue = 5051
    origins = [
        "http://localhost",
        f"http://localhost:{port_vue}",
    ]


class ConfigPathes:
    storage = Path("storage")
    models = storage / "models"
    snapshots = storage / "snapshots"


class ConfigDatabase:
    name = "database.db"


class ConfigModel:
    default = "yolo11l_100.pt"
    confidence = 0.75
    detecting_delay = 2 #sec


class ConfigRouters:
    classes_name = "classes"
    snapshots_name = "snapshots"
    cameras_name = "cameras"
    websockets_name = "ws"


class Config:
    app = ConfigApp()
    pathes = ConfigPathes()
    database = ConfigDatabase()
    model = ConfigModel()
    templates = Jinja2Templates(directory="static/html")
    routers = ConfigRouters()
