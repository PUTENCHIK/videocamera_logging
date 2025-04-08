import asyncio
from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import Config
from src.database import get_db_session
from src.cameras import (CameraAddOrEdit, Camera, CameraAfterEdit,
                         _add_camera, _get_cameras, _get_camera,
                         _edit_camera, _delete_camera, _switch_camera,
                         _restore_camera)
from src.detecting import task_manager


cameras_router = APIRouter(prefix=f"/{Config.routers.cameras_name}",
                           tags=[Config.routers.cameras_name])


@cameras_router.post("/add", response_model=Optional[Camera])
async def add_camera(fields: CameraAddOrEdit,
                     db: AsyncSession = Depends(get_db_session)):
    new_camera = await _add_camera(fields, db)
    return new_camera


@cameras_router.get("", response_model=List[Camera])
async def get_cameras(db: AsyncSession = Depends(get_db_session)):
    cameras = await _get_cameras(db)
    return cameras


@cameras_router.get("/{camera_id}", response_model=Optional[Camera])
async def get_camera(camera_id: int,
                     db: AsyncSession = Depends(get_db_session)):
    camera = await _get_camera(camera_id, db)
    return camera


@cameras_router.patch("/{camera_id}/edit", response_model=CameraAfterEdit)
async def edit_camera(camera_id: int,
                      fields: CameraAddOrEdit,
                      db: AsyncSession = Depends(get_db_session)):
    db_camera = await _get_camera(camera_id, db)

    result = CameraAfterEdit()
    if db_camera is not None:
        edited_camera = await _edit_camera(camera_id, fields, db)
        result.success = True
        result.camera = edited_camera
        asyncio.create_task(task_manager.edit_camera(edited_camera))
    
    return result


@cameras_router.patch("/{camera_id}/switch", response_model=CameraAfterEdit)
async def switch_camera(camera_id: int,
                        db: AsyncSession = Depends(get_db_session)):
    db_camera = await _get_camera(camera_id, db)

    result = CameraAfterEdit()
    if db_camera is not None:
        switched_camera = await _switch_camera(camera_id, db_camera.is_monitoring, db)
        result.success = True
        result.camera = switched_camera
        asyncio.create_task(task_manager.switch_camera(switched_camera))
    
    return result


@cameras_router.delete("/{camera_id}/delete", response_model=CameraAfterEdit)
async def delete_camera(camera_id: int,
                        db: AsyncSession = Depends(get_db_session)):
    db_camera = await _get_camera(camera_id, db)

    result = CameraAfterEdit()
    if db_camera is not None:
        deleted_camera = await _delete_camera(camera_id, db)
        result.success = True
        asyncio.create_task(task_manager.delete_camera(deleted_camera))
    
    return result


@cameras_router.patch("/{camera_id}/restore", response_model=Camera)
async def restore_camera(camera_id: int,
               db: AsyncSession = Depends(get_db_session)):
    restored_camera = await _restore_camera(camera_id, db)
    return restored_camera
