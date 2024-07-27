from pydantic import BaseModel


class DeviceCategorySchema(BaseModel):
  id: int
  name: str
  is_active: bool
  total_devices: int = 0

  class Config:
    orm_mode = True

class DeviceCategoryCreateSchema(BaseModel):
  name: str
  is_active: bool
