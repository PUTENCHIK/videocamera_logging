import uvicorn
from src import Config


if __name__ == "__main__":
    uvicorn.run(app=Config.app_name,
                host=Config.app_host,
                port=Config.app_port,
                reload_includes=["*.html", "*.css", "*.js"],
                reload_dirs=["static/css", "static/images"],
                reload=True)
