from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from src import Config
from src.database import DBSession, get_db_session
from src.cameras import _get_cameras


api_router = APIRouter()
router_path = "/api"


@api_router.get(f"{router_path}/cameras", response_class=JSONResponse)
async def get_cameras(request: Request, db: DBSession = Depends(get_db_session)):
    cameras = _get_cameras(db)
    json_cameras = jsonable_encoder(cameras)

    return JSONResponse(content=json_cameras)
