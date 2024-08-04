from typing import Any, List
from pydantic import BaseModel

from app.services.customer.customer_schema import CustomerBase
from app.services.users.user_schema import UserBase


class NotifySchemaBase(BaseModel):
    id: int
    customer: CustomerBase
    title: str
    content: str
    is_read: bool
    created_at: Any
    confirmed_at: Any
    explain: str | None
    user_verifier: UserBase | None = None


class NotifySchemaCreate(BaseModel):
    customer_id: int = "100"
    title: str = "Tiêu đề thông báo"
    content: str = "Nội dung thông báo"


class NotifySchemaUpdate(BaseModel):
    explain: str = "Giải thích thông báo"
