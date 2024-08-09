from typing import Optional
from pydantic import BaseModel, EmailStr


class CameraCreateSchema(BaseModel):
    name: str = "Camera nhà ăn"
    location_code: str = "D6"
    location: str = "Nhà ăn"
    stream_url: str | None = ""


class CameraSchema(CameraCreateSchema):
    id: int = 1
    status: str = "active"


class CameraUpdateSchema(BaseModel):
    name: Optional[str] = None
    location_code: Optional[str] = None
    location: Optional[str] = None
    stream_url: Optional[str] = None
    status: Optional[int] = 1
