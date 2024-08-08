from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, UploadFile

from app.core.dependencies import get_db
from sqlalchemy.orm import Session

from app.services.auth.authorize import get_current_active_user
from app.services.devices.device_schema import (
    DeviceCoreSchema,
    DeviceCreateResponse,
    DeviceCreateSchema,
    DeviceCreateSchemaFull,
    DeviceUpdateResponse,
    DeviceUpdateSchema,
    DeviceUpdateSchemaFull,
)
from app.services.devices.device_service import DeviceService
from app.services.users.user_schema import UserBase


router = APIRouter(prefix="/device", tags=["device"])

device_service = DeviceService()


@router.get("/health")
def get_health():
    return device_service.get_heath()


@router.get("", response_model=list[DeviceCoreSchema])
def get_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return device_service.get_devices(db, skip, limit)


@router.get("/{device_id}", response_model=DeviceCoreSchema)
def get_device(device_id: int, db: Session = Depends(get_db)):
    device = device_service.get_device(db, device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.post("/presigned_url/{presigned_url_id}")
def upload_image_presigned_url(
    presigned_url_id: str, file: UploadFile, db: Session = Depends(get_db)
):
    return device_service.upload_image(db, presigned_url_id, file)


@router.post("", response_model=DeviceCreateResponse)
def create_device(device: DeviceCreateSchema, db: Session = Depends(get_db)):
    # check device exist
    device_exist = device_service.get_device_by_name(db, device.name)
    if device_exist:
        raise HTTPException(status_code=409, detail="Device already exist")
    device_full = DeviceCreateSchemaFull(**device.dict(), presigned_url=None)
    return device_service.create_device(db, device_full)


@router.put("/{device_id}", response_model=DeviceUpdateResponse)
def update_device(
    device_id: int, device: DeviceUpdateSchema, db: Session = Depends(get_db)
):
    device_exist = device_service.get_device_by_name(db, device.name)
    if device_exist and device_exist.id != device_id:
        raise HTTPException(status_code=409, detail="Device name already exist")
    device_full = DeviceUpdateSchemaFull(**device.dict(), presigned_url=None)
    return device_service.update_device(db, device_id, device_full)


@router.delete("/{device_id}")
def delete_device(
    current_user: Annotated[UserBase, Depends(get_current_active_user)],
    device_id: int,
    db: Session = Depends(get_db),
):
    return device_service.delete_device(db, device_id)
