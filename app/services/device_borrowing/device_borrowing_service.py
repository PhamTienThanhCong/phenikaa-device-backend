import datetime
import json
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.core.setting import get_setting
from app.services.customer.customer_service import CustomerService
from app.services.device_borrowing.device_borrowing_model import DeviceBorrowing
from app.services.device_borrowing.device_borrowing_schema import (
    DeviceBorrowingCreate,
    DeviceBorrowingUpdate,
)
from app.services.devices.device_service import DeviceService
from app.services.users.user_service import UserService


class DeviceBorrowingService:
    def __init__(self):
        self.base = get_setting()
        self.device = DeviceService()
        self.user = UserService()
        self.customer = CustomerService()

    def get_all_device_borrowing(self, db: Session, skip: int = 0, limit: int = 100):
        device_borrowings = (
            db.query(DeviceBorrowing)
            .order_by(DeviceBorrowing.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        user_ids = [device_borrowing.user_id for device_borrowing in device_borrowings]
        customer_ids = [
            device_borrowing.customer_id for device_borrowing in device_borrowings
        ]
        users = self.user.get_users_by_ids(db, user_ids)
        customers = self.customer.get_customer_by_ids(db, customer_ids)
        # get current date time
        current_time = datetime.datetime.now()
        # maping user to device_borrowing
        for device_borrowing in device_borrowings:
            device_data = json.loads(device_borrowing.devices)
            for user in users:
                if device_borrowing.user_id == user.id:
                    device_borrowing.user = user
                    break
            for customer in customers:
                if device_borrowing.customer_id == customer.id:
                    device_borrowing.customer = customer
                    break
            device_ids = [device.get("device_id") for device in device_data]
            devices = self.device.get_devices_by_ids(db, device_ids)
            for device in devices:
                for device_item in device_data:
                    if device.id == device_item.get("device_id"):
                        device_item["device"] = device
                        break
            device_borrowing.devices = device_data
            # check status of device borrowing and update status
            if device_borrowing.is_returned is False:
                returning_date = device_borrowing.returning_date
                if current_time > returning_date:
                    device_borrowing.status = "overdue"
                else:
                    device_borrowing.status = "borrowing"
            else:
                device_borrowing.status = "returned"

        return device_borrowings

    def get_device_borrowing_by_id(self, db: Session, device_borrowing_id: int):
        device_borrowing = (
            db.query(DeviceBorrowing)
            .filter(DeviceBorrowing.id == device_borrowing_id)
            .first()
        )
        if not device_borrowing:
            raise HTTPException(status_code=404, detail="Device borrowing not found")

        user = self.user.get_user_by_id(db, device_borrowing.user_id)
        customer = self.customer.get_user_by_id(db, device_borrowing.customer_id)
        device_data = json.loads(device_borrowing.devices)
        device_ids = [device.get("device_id") for device in device_data]
        devices = self.device.get_devices_by_ids(db, device_ids)

        device_borrowing.user = user
        device_borrowing.customer = customer

        for device in devices:
            for device_item in device_data:
                if device.id == device_item.get("device_id"):
                    device_item["device"] = device
                    break
        device_borrowing.devices = device_data
        current_time = datetime.datetime.now()
        if device_borrowing.is_returned is False:
            returning_date = device_borrowing.returning_date
            if current_time > returning_date:
                device_borrowing.status = "overdue"
            else:
                device_borrowing.status = "borrowing"
        else:
            device_borrowing.status = "returned"

        return device_borrowing

    def create_device_borrowing(
        self, db: Session, device_borrowing: DeviceBorrowingCreate
    ):
        data = device_borrowing.dict()
        device_data = data.get("devices")
        self.device.validate_device(db, data.get("devices"))
        self.user.validate_user(db, data.get("user_id"))
        self.customer.validate_customer(db, data.get("customer_id"))
        created_at = datetime.datetime.now()
        data["created_at"] = created_at
        data["devices"] = json.dumps(data["devices"])

        device_borrowing = DeviceBorrowing(**data)
        db.add(device_borrowing)
        db.commit()
        db.refresh(device_borrowing)
        self.device.update_device_quantity(db, device_data, True, False)
        return self.get_device_borrowing_by_id(db, device_borrowing.id)

    def update_device_borrowing(
        self,
        db: Session,
        device_borrowing_id: int,
        device_borrowing: DeviceBorrowingUpdate,
    ):
        data = device_borrowing.dict()
        self.device.validate_device(db, data.get("devices"))
        self.user.validate_user(db, data.get("user_id"))
        self.customer.validate_customer(db, data.get("customer_id"))

        data["devices"] = json.dumps(data["devices"])

        db.query(DeviceBorrowing).filter(
            DeviceBorrowing.id == device_borrowing_id
        ).update(data)
        db.commit()

        return self.get_device_borrowing_by_id(db, device_borrowing_id)

    def delete_device_borrowing(self, db: Session, device_borrowing_id: int):
        db.query(DeviceBorrowing).filter(
            DeviceBorrowing.id == device_borrowing_id
        ).delete()
        db.commit()
        return "ok"
