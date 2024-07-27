from typing import Any
from pydantic import BaseModel

from app.services.customer.customer_schema import CustomerBase
from app.services.devices.device_schema import DeviceCoreSchema
from app.services.users.user_schema import UserBase


class Devices(BaseModel):
    quantity: int
    device: DeviceCoreSchema


class DevicesCreate(BaseModel):
    device_id: int
    quantity: int


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


class DeviceBorrowingUpdate(DeviceBorrowingCreate):
    is_returned: bool
