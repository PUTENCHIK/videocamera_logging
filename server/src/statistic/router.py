from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from src import Config


statistic_router = APIRouter(prefix=f"/{Config.routers.statistic_name}",
                             tags=[Config.routers.statistic_name])
