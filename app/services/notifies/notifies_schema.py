from typing import Any, List
from pydantic import BaseModel

from app.services.customer.customer_schema import CustomerBase
from app.services.users.user_schema import UserBase


class DeviceUserInfo(BaseModel):
    browser: str = "Chrome"
    browser_version: str = "90.0.4430.93"
    os: str = "Windows"
    os_version: str = "10"
    device: str = "Computer"


class LocationInfo(BaseModel):
    ip: str = "127.0.0.1"
    location: dict = {
        "ip": "127.0.0.1",
        "city": "Hanoi",
        "region": "Hanoi",
        "country": "VN",
        "loc": "21.0245,105.8412",
        "org": "AS18403 FPT Telecom Company",
        "postal": "10000",
        "timezone": "Asia/Bangkok",
    }
    device: DeviceUserInfo


class NotifySchemaBase(BaseModel):
    id: int
    customer: CustomerBase
    title: str
    category: str
    content: str
    status: str
    created_at: Any
    confirmed_at: Any
    explain: str | None = None
    user_verifier: UserBase | None = None
    location_info: LocationInfo


class NotifySchemaCreate(BaseModel):
    customer_id: int = "100"
    title: str = "Tiêu đề thông báo"
    category: str = "Loại thông báo"
    content: str = "Nội dung thông báo"


class NotifySchemaUpdate(BaseModel):
    explain: str = "Giải thích thông báo"


class NotifyCancelSchemaBase(BaseModel):
    customer_id: int = "100"
    birth_date: str = "01-01-2001"
