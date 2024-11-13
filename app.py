from pathlib import Path

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from src import (
    images_router,
    cameras_router,
    statistic_router,
    about_router
)

from src import Config


app = FastAPI()

app.include_router(images_router)
app.include_router(cameras_router)
app.include_router(statistic_router)
app.include_router(about_router)

app.mount("/static", StaticFiles(directory=Path("static")), name="static")
app.mount("/static/css", StaticFiles(directory=Path("static/css")), name="styles")
app.mount("/static/images", StaticFiles(directory=Path("static/images")), name="images")
app.mount("/static/js", StaticFiles(directory=Path("static/js")), name="scripts")
app.mount("/storage", StaticFiles(directory=Path("storage")), name="storage")


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
