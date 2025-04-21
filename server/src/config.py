from pathlib import Path


class ConfigApp:
    name = "src.app:app"
    host = "localhost"
    port = 5050
    port_vue = 5051
    origins = [
        "http://localhost",
        f"http://localhost:{port_vue}",
    ]
    max_detecting_workers = 4


class ConfigPathes:
    storage = Path("storage")
    models = storage / "models"
    snapshots = storage / "snapshots"


class ConfigDatabase:
    name = "database.db"


class ConfigDetecting:
    model_name = "yolo11l_100.pt"
    confidence = 0.75
    delay = 2 #sec
    cooldown = 15 #sec


class ConfigRouters:
    classes_name = "classes"
    snapshots_name = "snapshots"
    cameras_name = "cameras"
    websockets_name = "ws"


class Config:
    app = ConfigApp()
    pathes = ConfigPathes()
    database = ConfigDatabase()
    detecting = ConfigDetecting()
    routers = ConfigRouters()
