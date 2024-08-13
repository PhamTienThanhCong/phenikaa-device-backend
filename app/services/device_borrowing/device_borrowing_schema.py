from typing import Any
from pydantic import BaseModel

from app.services.customer.customer_schema import CustomerBase
from app.services.devices.device_schema import DeviceCoreSchema
from app.services.users.user_schema import UserBase


class Devices(BaseModel):
    quantity: int
    device: DeviceCoreSchema
    quantity_return: int = 0
    quantity_no_return: int = 0
    status: str = "borrowing"
    note: str = ""


class DevicesCreate(BaseModel):
    device_id: int
    quantity: int


class DevicesUpdate(BaseModel):
    device_id: int
    quantity_return: int
    status: str
    note: str


class DeviceBorrowingSchema(BaseModel):
    id: int
    name: str
    devices: list[Devices]
    user: UserBase
    customer: CustomerBase
    note: str
    returning_date: Any = "2024-01-01 00:00:00"
    is_returned: bool
    status: str
    retired_date: Any = "2024-01-01 00:00:00"
    created_at: Any = "2024-01-01 00:00:00"


class DeviceBorrowingCreate(BaseModel):
    name: str
    devices: list[DevicesCreate]
    user_id: int
    customer_id: int
    note: str
    returning_date: str = "2024-01-01 00:00:00"


class DeviceBorrowingUpdate(BaseModel):
    devices: list[DevicesUpdate]
    note: str
