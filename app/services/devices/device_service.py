from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from PIL import Image

from app.core.setting import get_setting
from app.services.devices.device_model import Device
from app.services.devices.device_schema import (
    DeviceCreateSchemaFull,
    DeviceUpdateSchemaFull,
)

import uuid

from app.utils.save_file import save_file_image


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
        if device.image:
            device.presigned_url = str(uuid.uuid4())

        device.image = "default.jpg"

        db_device = Device(**device.dict())
        db.add(db_device)
        db.commit()
        db.refresh(db_device)

        db_device.presigned_url = (
            f"{self.base['base_url']}/v1/device/presigned_url/{db_device.presigned_url}"
        )

        return db_device

    def update_device(
        self, db: Session, device_id: int, device: DeviceUpdateSchemaFull
    ):
        if device.image:
            device.image = ""
            device.presigned_url = str(uuid.uuid4())

        del device.image

        db.query(Device).filter(Device.id == device_id).update(device.dict())
        db.commit()

        db_device = db.query(Device).filter(Device.id == device_id).first()
        db_device.presigned_url = (
            f"{self.base['base_url']}/v1/device/presigned_url/{db_device.presigned_url}"
        )
        return db_device

    def delete_device(self, db: Session, device_id: int):
        db.query(Device).filter(Device.id == device_id).delete()
        db.commit()
        return {"message": "Device deleted successfully"}

    def upload_image(self, db: Session, presigned_url_id: str, file: UploadFile):
        # find device by presigned_url_id
        # check if file is image type

        device = (
            db.query(Device).filter(Device.presigned_url == presigned_url_id).first()
        )
        if device is None:
            raise HTTPException(status_code=404, detail="Device not found")

        file_path = f"/public/device/device_{device.id}.jpg"

        # update image path to device
        save_file_image(file, file_path)

        db.query(Device).filter(Device.id == device.id).update(
            {"image": file_path, "presigned_url": ""}
        )
        db.commit()
        return {"message": "Image uploaded successfully"}
