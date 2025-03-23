from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from src import Config


snapshots_router = APIRouter()
router_path = "/snapshots"


@snapshots_router.get(f"{router_path}", response_class=HTMLResponse)
async def index(request: Request):
    return Config.templates.TemplateResponse(
        request=request, name="snapshots.html"
    )
