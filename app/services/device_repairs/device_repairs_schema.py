from typing import Any
from pydantic import BaseModel

from app.services.devices.device_schema import DeviceCoreSchema
from app.services.maintenance_services.maintenance_services_schema import (
    MaintenanceServiceBase,
)
from app.services.users.user_schema import UserBase


class Devices(BaseModel):
    quantity: int
    device: DeviceCoreSchema
    cost_per_unit: int


class DevicesCreate(BaseModel):
    device_id: int
    quantity: int
    cost_per_unit: int


class DeviceRepairsSchema(BaseModel):
    id: int
    name: str
    is_returned: bool
    devices: list[Devices]
    user: UserBase
    service: MaintenanceServiceBase
    returning_date: Any = "2024-01-01 00:00:00"
    retired_date: Any = "2024-01-01 00:00:00"
    created_at: Any = "2024-01-01 00:00:00"
    status: str
    total_cost: int
    note: str


class DeviceRepairsCreate(BaseModel):
    name: str
    devices: list[DevicesCreate]
    user_id: int
    service_id: int
    returning_date: Any = "2024-01-01 00:00:00"
    note: str


class DeviceRepairsUpdate(DeviceRepairsCreate):
    is_returned: bool
