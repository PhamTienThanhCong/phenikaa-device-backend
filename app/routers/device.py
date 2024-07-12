from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_db
from sqlalchemy.orm import Session

from app.services.devices.device_schema import DeviceCoreSchema, DeviceCreateSchema, DeviceUpdateSchema
from app.services.devices.device_service import DeviceService


router = APIRouter( 
  prefix="/device",
  tags=["device"]
)

device_service = DeviceService()

@router.get("/health")
def get_health():
  return device_service.get_heath()

@router.get("/", response_model=list[DeviceCoreSchema])
def get_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  return device_service.get_devices(db, skip, limit)

@router.get("/{device_id}", response_model=DeviceCoreSchema)
def get_device(device_id: int, db: Session = Depends(get_db)):
  device = device_service.get_device(db, device_id)
  if device is None:
    raise HTTPException(status_code=404, detail="Device not found")
  return device

@router.post("/", response_model=DeviceCoreSchema)
def create_device(device: DeviceCreateSchema, db: Session = Depends(get_db)):
  # check device exist
  device_exist = device_service.get_device_by_name(db, device.name)
  if device_exist:
    raise HTTPException(status_code=409, detail="Device already exist")
  return device_service.create_device(db, device)

@router.put("/{device_id}", response_model=DeviceCoreSchema)
def update_device(device_id: int, device: DeviceUpdateSchema, db: Session = Depends(get_db)):
  device_exist = device_service.get_device_by_name(db, device.name)
  if device_exist and device_exist.id != device_id:
    raise HTTPException(status_code=409, detail="Device name already exist")
  return device_service.update_device(db, device_id, device)


@router.delete("/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db)):
  return device_service.delete_device(db, device_id)