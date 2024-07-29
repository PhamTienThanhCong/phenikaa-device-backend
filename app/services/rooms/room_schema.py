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
    room_id: str
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
