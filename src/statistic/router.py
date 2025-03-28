from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from src import Config


statistic_router = APIRouter(prefix=f"/{Config.routers.statistic_name}",
                             tags=[Config.routers.statistic_name])


@statistic_router.get("", response_class=HTMLResponse)
async def index(request: Request):
    return Config.templates.TemplateResponse(
        request=request, name="statistic.html"
    )
