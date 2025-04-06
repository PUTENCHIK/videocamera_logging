from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import Config
from src.database import get_db_session
from src.classes import (TrackableClassAddOrEdit, TrackableClassFull, TrackableClassAfterEdit,
                         _add_class, _get_class, _get_classes, _edit_class, _delete_class)


classes_router = APIRouter(prefix=f"/{Config.routers.classes_name}",
                           tags=[Config.routers.classes_name])


@classes_router.post("/add", response_model=Optional[TrackableClassFull])
async def add_class(class_: TrackableClassAddOrEdit,
                    db: AsyncSession = Depends(get_db_session)):
    new_class = await _add_class(class_, db)
    return new_class


@classes_router.get("", response_model=List[TrackableClassFull])
async def get_classes(db: AsyncSession = Depends(get_db_session)):
    classes = await _get_classes(db)
    return classes


@classes_router.patch("/{class_id}/edit", response_model=TrackableClassAfterEdit)
async def edit_class(class_id: int,
                     fields: TrackableClassAddOrEdit,
                     db: AsyncSession = Depends(get_db_session)):
    db_class = await _get_class(class_id, db)

    result = TrackableClassAfterEdit()
    if db_class is not None:
        edited_class = await _edit_class(class_id, fields, db)
        result.success = True
        result.class_ = edited_class
    
    return result


@classes_router.delete("/{class_id}/delete", response_model=TrackableClassAfterEdit)
async def delete_class(class_id: int,
                       db: AsyncSession = Depends(get_db_session)):
    db_class = await _get_class(class_id, db)

    result = TrackableClassAfterEdit()
    if db_class is not None:
        await _delete_class(class_id, db)
        result.success = True
    
    return result
