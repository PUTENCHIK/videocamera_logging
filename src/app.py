import asyncio

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from src import (
    Config, classes_router, snapshots_router, cameras_router,
    statistic_router, about_router, api_router
)
from src.detecting import task_manager
from src.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App starting")
    Config.pathes.snapshots.mkdir(exist_ok=True)
    await create_db_and_tables()        
    asyncio.create_task(task_manager.start())
    print("Cameras task added")
    yield
    print("App terminating")
    await task_manager.kill_task()


app = FastAPI(lifespan=lifespan)

app.include_router(classes_router)
app.include_router(snapshots_router)
app.include_router(cameras_router)
app.include_router(statistic_router)
app.include_router(about_router)
app.include_router(api_router)

app.mount("/static", StaticFiles(directory=Config.pathes.static), name="static")
app.mount("/static/css", StaticFiles(directory=Config.pathes.css), name="styles")
app.mount("/static/images", StaticFiles(directory=Config.pathes.images), name="images")
app.mount("/static/js", StaticFiles(directory=Config.pathes.js), name="scripts")
app.mount("/storage", StaticFiles(directory=Config.pathes.storage), name="storage")
app.mount("/static/images/icons", StaticFiles(directory=Config.pathes.icons), name="icons")
app.mount("/storage/snapshots", StaticFiles(directory=Config.pathes.snapshots), name="snapshots")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(Config.pathes.icons / Config.app.icon)


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
