from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile

from app.core.dependencies import get_db
from sqlalchemy.orm import Session

from app.services.auth.authorize import get_current_active_user
from app.services.device_repairs.device_repairs_schema import (
    DeviceRepairsCreate,
    DeviceRepairsSchema,
    DeviceRepairsUpdate,
)
from app.services.device_repairs.device_repairs_service import DeviceRepairsService

router = APIRouter(prefix="/device-repair", tags=["device-repair"])

device_repair = DeviceRepairsService()


@router.get("/health")
def get_health():
    return "OK"


@router.get("")
def get_all_device_repairs(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    return device_repair.get_all_device_repairs(db, skip, limit)


@router.get("/{device_repair_id}", response_model=DeviceRepairsSchema)
def get_device_repair_by_id(
    device_repair_id: int,
    db: Session = Depends(get_db),
):
    service = device_repair.get_device_repair_by_id(db, device_repair_id)
    if not service:
        raise HTTPException(status_code=404, detail="Device repair not found")
    return service


@router.post("")
def create_device_repair(
    device_repair_payload: DeviceRepairsCreate,
    db: Session = Depends(get_db),
):
    return device_repair.create_device_repair(db, device_repair_payload)


@router.put("/{device_repair_id}", response_model=DeviceRepairsSchema)
def update_device_repair(
    device_repair_id: int,
    device_repair_payload: DeviceRepairsUpdate,
    db: Session = Depends(get_db),
):
    return device_repair.update_device_repair(
        db, device_repair_id, device_repair_payload
    )


@router.delete("/{device_repair_id}")
def delete_device_repair(
    device_repair_id: int,
    db: Session = Depends(get_db),
):
    return device_repair.delete_device_repair(db, device_repair_id)
