from pathlib import Path

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from src import (
    Config,
    images_router,
    cameras_router,
    statistic_router,
    about_router,
    api_router,
    DetectingModel
)

from src.database import BaseDBModel, engine


app = FastAPI()
model = DetectingModel()

# from pathlib import Path
# import cv2
# import random
# storage_path = Path("storage")
# pathes = [path for path in storage_path.glob("*.*") if path.suffix in ['.png', '.jpg', '.jpeg']]
# images = [cv2.imread(path) for path in pathes]

BaseDBModel.metadata.create_all(bind=engine)

app.include_router(images_router)
app.include_router(cameras_router)
app.include_router(statistic_router)
app.include_router(about_router)
app.include_router(api_router)

app.mount("/static", StaticFiles(directory=Path("static")), name="static")
app.mount("/static/css", StaticFiles(directory=Path("static/css")), name="styles")
app.mount("/static/images", StaticFiles(directory=Path("static/images")), name="images")
app.mount("/static/js", StaticFiles(directory=Path("static/js")), name="scripts")
app.mount("/storage", StaticFiles(directory=Path("storage")), name="storage")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return Config.templates.TemplateResponse(
        request=request, name="index.html"
    )

# @app.get("/predict")
# async def predict():
#     image = random.choice(images)
#     result = model.predict(image)
#     return {"response": result.to_json()}


@app.get("/{any}")
async def other(any: str):
    raise Exception(f"No such path: {any}")


@app.exception_handler(Exception)
async def exception_handler(request: Request, ex: Exception):
    return JSONResponse(
        status_code=404,
        content=str(ex)
    )
