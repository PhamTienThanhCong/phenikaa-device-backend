from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException

from app.core.dependencies import get_db
from app.services.auth.authorize import get_current_active_user
from sqlalchemy.orm import Session

from app.services.camera.camera_schema import (
    CameraCreateSchema,
    CameraSchema,
    CameraUpdateSchema,
)
from app.services.camera.camera_service import CameraService


router = APIRouter(prefix="/camera", tags=["camera service"])

customer_service = CameraService()


@router.get("", response_model=list[CameraSchema])
def get_all_cameras(db: Session = Depends(get_db)):
    return customer_service.get_all(db)


@router.post("", response_model=CameraSchema)
def create_camera(camera: CameraCreateSchema, db: Session = Depends(get_db)):
    return customer_service.create(db, camera)


@router.put("/{camera_id}", response_model=CameraSchema)
def update_camera(
    camera_id: int, camera: CameraUpdateSchema = Body(), db: Session = Depends(get_db)
):
    return customer_service.update(db, camera_id, camera)


@router.delete("/{camera_id}")
def delete_camera(camera_id: int, db: Session = Depends(get_db)):
    return customer_service.delete(db, camera_id)
