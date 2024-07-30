from typing import Any, List
from pydantic import BaseModel

from app.services.customer.customer_schema import CustomerBase
from app.services.rooms.room_schema import RoomSchemaBase
from app.services.users.user_schema import UserBase


class RoomBookingSchemaBase(BaseModel):
    id: int
    name: str
    room: RoomSchemaBase
    user: UserBase
    customer: CustomerBase
    total_customer: int
    date_booking: Any
    start_time: Any
    end_time: Any
    note: str
    created_at: Any
    updated_at: Any
    status: str
    is_active: bool


class RoomBookingSchemaCreate(BaseModel):
    name: str = "Mượn phòng học A2-101"
    room_id: str = "A2-101"
    user_id: int = 8
    customer_id: int = 101
    total_customer: int = 1
    date_booking: str = "2024-01-01"
    start_time: str = "12:00:00"
    end_time: str = "16:00:00"
    note: str = "con cac."


class RoomBookingSchemaUpdate(BaseModel):
    name: str = "Mượn phòng học A2-101"
    room_id: str = "A2-101"
    total_customer: int = 1
    date_booking: str = "2024-01-01"
    start_time: str = "12:00:00"
    end_time: str = "16:00:00"
    note: str = "con cac."
    is_active: bool = True
