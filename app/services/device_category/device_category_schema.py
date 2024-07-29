from pydantic import BaseModel


class DeviceCategorySchema(BaseModel):
    id: int
    name: str
    is_active: bool
    total_devices: int = 0
    image: str = "default.jpg"
    presigned_url: str = ""


class DeviceCategoryCreateSchema(BaseModel):
    name: str
    is_active: bool
    image: str = ""
