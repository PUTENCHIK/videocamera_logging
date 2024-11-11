from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from src import Config


statistic_router = APIRouter()
router_path = "/statistic"


@statistic_router.get(f"{router_path}", response_class=HTMLResponse)
async def index(request: Request):
    return Config.templates.TemplateResponse(
        request=request, name="statistic.html"
    )
