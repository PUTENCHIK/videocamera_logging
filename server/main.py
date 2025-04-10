import uvicorn
from src import Config


if __name__ == "__main__":
    Config.pathes.storage.mkdir(exist_ok=True)
    Config.pathes.models.mkdir(exist_ok=True)
    Config.pathes.snapshots.mkdir(exist_ok=True)
    uvicorn.run(app=Config.app.name,
                host=Config.app.host,
                port=Config.app.port,
                reload=True)
