from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from src import Config


snapshots_router = APIRouter(prefix=f"/{Config.routers.snapshots_name}",
                             tags=[Config.routers.snapshots_name])
