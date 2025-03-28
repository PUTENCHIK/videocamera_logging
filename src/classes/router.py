import asyncio
from typing import Optional
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src import Config
from src.database import get_db_session
from src.classes import (TrackableClassAddOrEdit, TrackableClassFull, TrackableClassAfterEdit,
                         _add_class, _get_class, _edit_class, _delete_class)
from src.detecting import task_manager


router_name = "classes"
classes_router = APIRouter(prefix=f"/{router_name}", tags=[router_name])


@classes_router.get("", response_class=HTMLResponse)
async def index(request: Request):
    return Config.templates.TemplateResponse(
        request=request,
        name="classes.html"
    )


@classes_router.post("/add", response_model=Optional[TrackableClassFull])
async def add_class(class_: TrackableClassAddOrEdit, db: AsyncSession = Depends(get_db_session)):
    new_class = await _add_class(class_, db)
    return new_class


@classes_router.patch("/{class_id}/edit", response_model=TrackableClassAfterEdit)
async def edit_class(class_id: int, fields: TrackableClassAddOrEdit, db: AsyncSession = Depends(get_db_session)):
    db_class = await _get_class(class_id, db)

    result = TrackableClassAfterEdit()
    if db_class is not None:
        edited_class = await _edit_class(db_class, fields, db)
        result.success = True
        result.class_ = edited_class
    
    return result


@classes_router.delete("/{class_id}/delete", response_model=TrackableClassAfterEdit)
async def delete_class(class_id: int, db: AsyncSession = Depends(get_db_session)):
    db_class = await _get_class(class_id, db)

    result = TrackableClassAfterEdit()
    if db_class is not None:
        await _delete_class(db_class, db)
        result.success = True
    
    return result
