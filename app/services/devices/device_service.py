from typing import List
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

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

    def validate_device(self, db: Session, devices: list):
        for device in devices:
            device_id = device.get("device_id")
            device_exist = self.get_device(db, device_id)
            if device_exist is None:
                raise HTTPException(status_code=404, detail="Device not found")
            device_exist_quantity = (
                device_exist.total
                - device_exist.total_used
                - device_exist.total_maintenance
            )
            if device_exist_quantity < device.get("quantity"):
                raise HTTPException(status_code=400, detail="Quantity not enough")
            if device_exist.is_active is False:
                raise HTTPException(status_code=400, detail="Device is not active")
        return True

    def update_device_quantity(
        self, db: Session, devices: list, is_borrowing: bool, is_returned: bool
    ):
        for device in devices:
            device_id = device.get("device_id")
            quantity = device.get("quantity")
            device_exist = self.get_device(db, device_id)

            if is_returned:
                if is_borrowing:
                    device_exist.total_used = device_exist.total_used - quantity
                else:
                    device_exist.total_maintenance = (
                        device_exist.total_maintenance - quantity
                    )
            else:
                if is_borrowing:
                    device_exist.total_used = device_exist.total_used + quantity
                else:
                    device_exist.total_maintenance = (
                        device_exist.total_maintenance + quantity
                    )

            # update data to db
            db.query(Device).filter(Device.id == device_id).update(
                {
                    "total_used": device_exist.total_used,
                    "total_maintenance": device_exist.total_maintenance,
                }
            )

        db.commit()
        return True

    def return_device_maintenance(self, db: Session, devices: list):
        for device in devices:
            device_id = device.get("device_id")
            quantity_done = device.get("quantity")
            device_exist = self.get_device(db, device_id)
            device_exist.total_maintenance = (
                device_exist.total_maintenance - quantity_done
            )
            db.query(Device).filter(Device.id == device_id).update(
                {"total_maintenance": device_exist.total_maintenance}
            )

        db.commit()
        return True

    def get_devices_by_ids(self, db: Session, device_ids: List[int]):
        return db.query(Device).filter(Device.id.in_(device_ids)).all()

    def count_devices(self, db: Session, category: List[str]):
        total_devices = {}
        for cat in category:
            total_devices[cat] = db.query(Device).filter(Device.category == cat).count()
        return total_devices

    def get_device(self, db: Session, device_id: int):
        return db.query(Device).filter(Device.id == device_id).first()

    def get_devices(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Device).offset(skip).limit(limit).all()

    def get_device_by_name(self, db: Session, name: str):
        return db.query(Device).filter(Device.name == name).first()

    def create_device(self, db: Session, device: DeviceCreateSchemaFull):
        if device.image:
            device.presigned_url = str(uuid.uuid4())

        device.image = "/public/device/default.jpg"

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
