from pydantic import BaseModel


class DeviceCoreSchema(BaseModel):
  id: int
  name: str
  category: str
  information: str
  note: str
  total: int
  total_used: int
  total_maintenance: int
  is_active: int


class DeviceCreateSchema(BaseModel):
  name: str
  category: str
  information: str
  note: str
  total: int

class DeviceUpdateSchema(BaseModel):
  name: str | None 
  category: str | None 
  information: str | None 
  note: str | None 
  total: int | None 
  total_used: int | None 
  total_maintenance: int | None 
  is_active: bool | None 
