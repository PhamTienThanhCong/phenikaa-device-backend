from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile

from app.core.dependencies import get_db
from sqlalchemy.orm import Session

from app.services.auth.authorize import get_current_active_user
from app.services.maintenance_services.maintenance_services_schema import (
    MaintenanceServiceBase,
    MaintenanceServicePayload,
)
from app.services.maintenance_services.maintenance_services_service import (
    MaintenanceServicesService,
)


router = APIRouter(prefix="/maintenance", tags=["maintenance"])

device_service = MaintenanceServicesService()


@router.get("/health")
def get_health():
    return device_service.get_health()


@router.get("", response_model=List[MaintenanceServiceBase])
def get_all_services(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return device_service.get_all_services(db, skip, limit)


@router.get("/{service_id}", response_model=MaintenanceServiceBase)
def get_service_by_id(service_id: int, db: Session = Depends(get_db)):
    service = device_service.get_service_by_id(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


@router.post("", response_model=MaintenanceServiceBase)
def create_service(service: MaintenanceServicePayload, db: Session = Depends(get_db)):
    try:
        return device_service.create_service(db, service)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Phone or email already exists")


@router.put("/{service_id}", response_model=MaintenanceServiceBase)
def update_service(
    service_id: int, service: MaintenanceServicePayload, db: Session = Depends(get_db)
):
    if not device_service.get_service_by_id(db, service_id):
        raise HTTPException(status_code=404, detail="Service not found")
    try:
        return device_service.update_service(db, service_id, service)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Phone or email already exists")


@router.delete("/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    if not device_service.get_service_by_id(db, service_id):
        raise HTTPException(status_code=404, detail="Service not found")
    return device_service.delete_service(db, service_id)
