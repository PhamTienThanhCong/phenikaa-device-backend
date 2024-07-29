from typing import List
from pydantic import BaseModel


class RoomSchemaUpdate(BaseModel):
    category: str
    house_name: str
    manager: str
    detail: List[dict] = [
        {
            "name": "table",
            "total": 10,
        },
        {
            "name": "chair",
            "total": 20,
        },
    ]
    note: str
    is_active: bool = True
    is_using: bool = False
    is_maintenance: bool = False


class RoomSchemaBase(RoomSchemaUpdate):
    room_id: str


class RoomSchemaCreate(BaseModel):
    room_id: str = "A2-101"
    category: str = "Giảng đường"
    house_name: str = "A2"
    manager: str = "Khoa CNTT - Trường ĐH Phenikaa"
    detail: List[dict] = [
        {
            "name": "Bàn",
            "total": 10,
        },
        {
            "name": "Ghế",
            "total": 20,
        },
    ]
    note: str = "Phòng học lớn phục vụ cho việc giảng dạy"
