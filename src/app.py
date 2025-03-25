from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from src import (
    Config,
    snapshots_router,
    cameras_router,
    statistic_router,
    about_router,
    api_router
)
from src.snapshots import add_trackable_classes
from src.detecting import start_camera_monitoring
from src.database import create_db_and_tables, get_db_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App starting")
    await create_db_and_tables()
    
    async for db in get_db_session():
        try:
            await add_trackable_classes(db)
        except Exception as e:
            print(f"Adding trackable classes failed: {e}")
            db.rollback()
    await start_camera_monitoring()
    print("Cameras' tasks added")
    yield
    print("App terminating")


app = FastAPI(lifespan=lifespan)

app.include_router(snapshots_router)
app.include_router(cameras_router)
app.include_router(statistic_router)
app.include_router(about_router)
app.include_router(api_router)

app.mount("/static", StaticFiles(directory=Path("static")), name="static")
app.mount("/static/css", StaticFiles(directory=Path("static/css")), name="styles")
app.mount("/static/images", StaticFiles(directory=Path("static/images")), name="images")
app.mount("/static/js", StaticFiles(directory=Path("static/js")), name="scripts")
app.mount("/storage", StaticFiles(directory=Path("storage")), name="storage")
app.mount("/static/images/icons", StaticFiles(directory=Path("static/images/icons")), name="icons")
app.mount("/storage/snapshots", StaticFiles(directory=Path("storage/snapshots")), name="snapshots")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(Config.app_icon)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return Config.templates.TemplateResponse(
        request=request, name="index.html"
    )


@app.get("/{any}")
async def other(any: str):
    raise Exception(f"No such path: {any}")


@app.exception_handler(Exception)
async def exception_handler(request: Request, ex: Exception):
    return JSONResponse(
        status_code=404,
        content=str(ex)
    )
