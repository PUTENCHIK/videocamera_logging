import uvicorn
from app import app
from src import Config


if __name__ == "__main__":
    try:
        uvicorn.run(Config.app_name, host=Config.app_host, port=Config.app_port, reload=True)
    except KeyboardInterrupt:
        print("Shutdown by keyboard interrupt")
    finally:
        exit()
