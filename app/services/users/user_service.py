from pydantic import BaseModel

class UserBase(BaseModel):
  id: int
  full_name: str
  email: str
  role: int
  is_active: bool

class UserCreate(UserBase):
  full_name: str