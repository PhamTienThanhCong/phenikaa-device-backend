import datetime
import json
from typing import List
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.core.setting import get_setting
import uuid

from app.services.device_repairs.device_repairs_model import DeviceRepairs
from app.services.device_repairs.device_repairs_schema import (
    DeviceRepairsCreate,
    DeviceRepairsUpdate,
)
from app.services.devices.device_service import DeviceService
from app.services.maintenance_services.maintenance_services_service import (
    MaintenanceServicesService,
)
from app.services.users.user_service import UserService


class DeviceRepairsService:
    def __init__(self):
        self.base = get_setting()
        self.device = DeviceService()
        self.user = UserService()
        self.service = MaintenanceServicesService()

    def get_heath(self):
        return JSONResponse(status_code=200, content={"status": "UP"})

    def get_all_device_repairs(self, db: Session, skip: int = 0, limit: int = 100):
        device_repairs = (
            db.query(DeviceRepairs)
            .order_by(DeviceRepairs.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        user_ids = [device_repair.user_id for device_repair in device_repairs]
        service_ids = [device_repair.service_id for device_repair in device_repairs]
        users = self.user.get_users_by_ids(db, user_ids)
        services = self.service.get_services_by_ids(db, service_ids)
        # get current date time
        current_time = datetime.datetime.now()
        # maping user to device_repair
        for device_repair in device_repairs:
            device_data = json.loads(device_repair.devices)
            total_cost = 0
            for user in users:
                if device_repair.user_id == user.id:
                    device_repair.user = user
                    break
            for service in services:
                if device_repair.service_id == service.id:
                    device_repair.service = service
                    break
            device_ids = [device.get("device_id") for device in device_data]
            devices = self.device.get_devices_by_ids(db, device_ids)
            for device in devices:
                for device_item in device_data:
                    if device.id == device_item.get("device_id"):
                        device_item["device"] = device
                        break
                total_cost += device_item.get("quantity") * device_item.get(
                    "cost_per_unit"
                )
            device_repair.devices = device_data
            # check status of device repair and update status
            if device_repair.is_returned == True:
                device_repair.status = "Returned"
            else:
                if device_repair.returning_date < current_time:
                    device_repair.status = "Overdue"
                else:
                    device_repair.status = "In progress"
            device_repair.total_cost = total_cost

        return device_repairs

    def get_device_repair_by_id(self, db: Session, device_repair_id: int):
        device_repair = (
            db.query(DeviceRepairs).filter(DeviceRepairs.id == device_repair_id).first()
        )
        if not device_repair:
            raise HTTPException(status_code=404, detail="Device repair not found")
        user = self.user.get_user_by_id(db, device_repair.user_id)
        service = self.service.get_service_by_id(db, device_repair.service_id)
        device_data = json.loads(device_repair.devices)

        total_cost = 0
        device_ids = [device.get("device_id") for device in device_data]
        devices = self.device.get_devices_by_ids(db, device_ids)
        for device in devices:
            for device_item in device_data:
                if device.id == device_item.get("device_id"):
                    device_item["device"] = device
                    break
            total_cost += device_item.get("quantity") * device_item.get("cost_per_unit")

        # current date time
        current_time = datetime.datetime.now()
        # check status of device repair and update status
        if device_repair.is_returned == True:
            device_repair.status = "Returned"
        else:
            if device_repair.returning_date < current_time:
                device_repair.status = "Overdue"
            else:
                device_repair.status = "In progress"

        device_repair.user = user
        device_repair.service = service
        device_repair.devices = device_data
        device_repair.total_cost = total_cost
        return device_repair

    def create_device_repair(self, db: Session, device_repair: DeviceRepairsCreate):
        data = device_repair.dict()
        device_data = data.get("devices")
        self.device.validate_device(db, device_data)
        self.user.validate_user(db, data.get("user_id"))
        self.service.validate_service(db, data.get("service_id"))
        created_at = datetime.datetime.now()
        data["created_at"] = created_at
        data["devices"] = json.dumps(data["devices"])

        db_device_repair = DeviceRepairs(**data)
        db.add(db_device_repair)
        db.commit()
        db.refresh(db_device_repair)
        self.device.update_device_quantity(db, device_data, False, False)
        return self.get_device_repair_by_id(db, db_device_repair.id)

    def update_device_repair(
        self, db: Session, device_repair_id: int, device_repair: DeviceRepairsUpdate
    ):
        # get device repair by id
        device_repair_request = (
            db.query(DeviceRepairs).filter(DeviceRepairs.id == device_repair_id).first()
        )
        data = device_repair.dict()
        device_data = data.get("devices")
        self.device.validate_device(db, device_data)
        self.user.validate_user(db, data.get("user_id"))
        self.service.validate_service(db, data.get("service_id"))

        device_revert = json.loads(device_repair_request.devices)
        self.device.update_device_quantity(db, device_revert, False, True)
        db.commit()
        self.device.update_device_quantity(db, device_data, False, False)
        data["devices"] = json.dumps(data["devices"])
        db.query(DeviceRepairs).filter(DeviceRepairs.id == device_repair_id).update(
            data, synchronize_session=False
        )
        return self.get_device_repair_by_id(db, device_repair_id)

    def delete_device_repair(self, db: Session, device_repair_id: int):
        device_repair = (
            db.query(DeviceRepairs).filter(DeviceRepairs.id == device_repair_id).first()
        )
        if not device_repair:
            raise HTTPException(status_code=404, detail="Device repair not found")
        db.delete(device_repair)
        db.commit()
        device_data = json.loads(device_repair.devices)
        self.device.update_device_quantity(db, device_data, False, True)

        return device_repair
