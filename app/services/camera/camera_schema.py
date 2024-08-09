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
    name: Optional[str] = "Camera nhà ăn"
    location_code: Optional[str] = "D6"
    location: Optional[str] = "Nhà ăn"
    stream_url: Optional[str] = ""
    status: Optional[int] = 1
