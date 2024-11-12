import uvicorn
from src import Config
from app import app


if __name__ == "__main__":
    uvicorn.run(Config.app_name,
                host=Config.app_host,
                port=Config.app_port,
                reload_includes=["*.html", "*.css", "*.js"],
                reload_dirs=["static/css", "static/images"],
                reload=True)
