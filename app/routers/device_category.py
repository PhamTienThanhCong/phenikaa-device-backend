from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, UploadFile

from app.core.dependencies import get_db
from sqlalchemy.orm import Session

from app.services.auth.authorize import get_current_active_user
from app.services.device_category.device_category_schema import (
    DeviceCategoryCreateSchema,
    DeviceCategorySchema,
)
from app.services.device_category.device_category_service import DeviceCategoryService


router = APIRouter(prefix="/device-category", tags=["category device"])

device_category_service = DeviceCategoryService()


@router.get("/", response_model=list[DeviceCategorySchema])
def get_all_category(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return device_category_service.get_all_category(db, skip, limit)


@router.get("/{category_id}", response_model=DeviceCategorySchema)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    device = device_category_service.get_category_by_id(db, category_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.post("/", response_model=DeviceCategorySchema)
def create_category(device: DeviceCategoryCreateSchema, db: Session = Depends(get_db)):
    # check device exist
    device_exist = device_category_service.get_category_by_name(db, device.name)
    if device_exist:
        raise HTTPException(status_code=409, detail="Device already exist")
    return device_category_service.create_category(db, device)


@router.put("/{category_id}", response_model=DeviceCategorySchema)
def update_category(
    category_id: int, device: DeviceCategoryCreateSchema, db: Session = Depends(get_db)
):
    device_exist = device_category_service.get_category_by_id(db, category_id)
    if device_exist is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return device_category_service.update_category(db, category_id, device)


@router.post("/presigned_url/{presigned_url_id}")
def upload_image_presigned_url(
    presigned_url_id: str, file: UploadFile, db: Session = Depends(get_db)
):
    return device_category_service.upload_image(db, presigned_url_id, file)
