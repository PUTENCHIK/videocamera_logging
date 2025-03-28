from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from src import Config


about_router = APIRouter(prefix=f"/{Config.routers.about_name}",
                         tags=[Config.routers.about_name])


@about_router.get("", response_class=HTMLResponse)
async def index(request: Request):
    return Config.templates.TemplateResponse(
        request=request, name="about.html"
    )
