from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.core.setting import get_setting
from app.services.devices.device_model import Device
from app.services.devices.device_schema import DeviceCreateSchema, DeviceCreateSchemaFull, DeviceUpdateSchema, DeviceUpdateSchemaFull

import uuid

class DeviceService:
  def __init__(self):
    self.base = get_setting()
    pass
  def get_heath(self):
    return JSONResponse(status_code=200, content={"status": "UP"})
  
  def get_device(self, db: Session, device_id: int):
    return db.query(Device).filter(Device.id == device_id).first()
  
  def get_devices(self, db: Session, skip: int = 0, limit: int = 100):
    return db.query(Device).offset(skip).limit(limit).all() 
  
  def get_device_by_name(self, db: Session, name: str):
    return db.query(Device).filter(Device.name == name).first()
  
  def create_device(self, db: Session, device: DeviceCreateSchemaFull):
    if (device.image):
      device.image = ""
      device.presigned_url = str(uuid.uuid4())

    db_device = Device(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)

    db_device.presigned_url = f"{self.base['base_url']}/v1/device/presigned_url/{db_device.presigned_url}"

    return db_device

  def update_device(self, db: Session, device_id: int, device: DeviceUpdateSchemaFull):
    if (device.image):
      device.image = ""
      device.presigned_url = str(uuid.uuid4())
    db.query(Device).filter(Device.id == device_id).update(device.dict())
    db.commit()

    db_device = db.query(Device).filter(Device.id == device_id).first()
    db_device.presigned_url = f"{self.base['base_url']}/v1/device/presigned_url/{db_device.presigned_url}"
    return db_device
  
  def delete_device(self, db: Session, device_id: int):
    db.query(Device).filter(Device.id == device_id).delete()
    db.commit()
    return {"message": "Device deleted successfully"}