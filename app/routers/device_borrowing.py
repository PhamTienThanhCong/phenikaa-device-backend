from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, UploadFile

from app.core.dependencies import get_db
from sqlalchemy.orm import Session

from app.services.auth.authorize import get_current_active_user
from app.services.device_borrowing.device_borrowing_schema import (
    DeviceBorrowingCreate,
    DeviceBorrowingSchema,
    DeviceBorrowingUpdate,
)
from app.services.device_borrowing.device_borrowing_service import (
    DeviceBorrowingService,
)

router = APIRouter(prefix="/device-borrowing", tags=["device-borrowing"])

device_service = DeviceBorrowingService()


@router.get("/health")
def get_health():
    return "OK"


@router.get("")
def get_all_device_borrowing(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    return device_service.get_all_device_borrowing(db, skip, limit)


@router.get("/{device_borrowing_id}", response_model=DeviceBorrowingSchema)
def get_device_borrowing_by_id(
    device_borrowing_id: int,
    db: Session = Depends(get_db),
):
    return device_service.get_device_borrowing_by_id(db, device_borrowing_id)


@router.post("", response_model=DeviceBorrowingSchema)
def create_device_borrowing(
    device_borrowing: DeviceBorrowingCreate,
    db: Session = Depends(get_db),
):
    return device_service.create_device_borrowing(db, device_borrowing)


@router.put("/{device_borrowing_id}")
def update_device_borrowing(
    device_borrowing_id: int,
    device_borrowing: DeviceBorrowingUpdate,
    db: Session = Depends(get_db),
):
    return device_service.update_device_borrowing(
        db, device_borrowing_id, device_borrowing
    )


@router.post("/{device_borrowing_id}/return")
def return_device_borrowing(
    device_borrowing_id: int,
    db: Session = Depends(get_db),
):
    return device_service.return_device_borrowing(db, device_borrowing_id)


@router.delete("/{device_borrowing_id}")
def delete_device_borrowing(
    device_borrowing_id: int,
    db: Session = Depends(get_db),
):
    return device_service.delete_device_borrowing(db, device_borrowing_id)
