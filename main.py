from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/static/css", StaticFiles(directory="static/css"), name="styles")

templates = Jinja2Templates(directory="static/html")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


@app.get("/{any}")
async def other(any: str):
    raise Exception("No such page")


@app.exception_handler(Exception)
async def exception_handler(request: Request, ex: Exception):
    return JSONResponse(
        status_code=404,
        content=str(ex)
    )
