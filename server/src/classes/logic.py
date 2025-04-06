import re

from typing import Optional, List, Dict
from datetime import datetime
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.classes import (Color, TrackableClassModel, TrackableClassAddOrEdit,
                         TrackableClass, TrackableClassFull, TrackableClassAfterEdit)


def _parse_color(color: str) -> Optional[Color]:
    result = re.match(r"^\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})$", color)
    if result is not None:
        r, g, b = result.groups()
        result = Color(r=int(r, 16),
                       g=int(g, 16),
                       b=int(b, 16))    
    return result


async def _add_class(fields: TrackableClassAddOrEdit,
                     db: AsyncSession) -> TrackableClassFull:
    color = _parse_color(fields.color)
    query = (insert(TrackableClassModel)
        .values(
            name=fields.name.lower(),
            label=int(fields.label),
            title=fields.title.lower(),
            color=color.model_dump(),
            created_at=datetime.now())
        .returning(TrackableClassModel))
    result = await db.execute(query)
    new_class = result.scalar_one()

    await db.commit()
    await db.refresh(new_class)

    return TrackableClassFull.model_validate(new_class)


async def _get_classes(db: AsyncSession) -> List[TrackableClassFull]:
    query = select(TrackableClassModel).where(TrackableClassModel.deleted_at == None)
    result = await db.execute(query)
    return [TrackableClassFull.model_validate(class_)
            for class_ in result.scalars().all()]


async def _get_class(id: int,
                     db: AsyncSession) -> Optional[TrackableClassFull]:
    query = (select(TrackableClassModel)
        .where(TrackableClassModel.deleted_at == None,
               TrackableClassModel.id == id))
    result = await db.execute(query)
    class_ = result.scalar_one_or_none()
    return TrackableClassFull.model_validate(class_) if class_ is not None else None


async def _edit_class(id: int,
                      fields: TrackableClassAddOrEdit,
                      db: AsyncSession) -> TrackableClassFull:
    color = _parse_color(fields.color)
    query = (update(TrackableClassModel)
        .where(TrackableClassModel.id == id)
        .values(name=fields.name.lower(),
                label=int(fields.label),
                title=fields.title.lower(),
                color=color.model_dump())
        .returning(TrackableClassModel))
    result = await db.execute(query)
    updated_class = result.scalar_one()

    await db.commit()
    await db.refresh(updated_class)

    return TrackableClassFull.model_validate(updated_class)


async def _delete_class(id: int,
                        db: AsyncSession) -> TrackableClassFull:
    query = (update(TrackableClassModel)
        .where(TrackableClassModel.id == id)
        .values(deleted_at=datetime.now())
        .returning(TrackableClassModel))
    result = await db.execute(query)
    deleted_class = result.scalar_one()

    await db.commit()
    await db.refresh(deleted_class)

    return TrackableClassFull.model_validate(deleted_class)
