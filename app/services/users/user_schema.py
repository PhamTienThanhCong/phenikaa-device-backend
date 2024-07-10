from pydantic import BaseModel, EmailStr

from app.enums.user_role import USER_ROLE

class UserBase(BaseModel):
  id: int
  full_name: str
  email: EmailStr | str
  role: USER_ROLE
  is_active: int
  class Config:
    use_enum_values = True

class UserCreate(BaseModel):
  full_name: str
  email: EmailStr
  role: USER_ROLE
  password: str
  class Config:
    use_enum_values = True

class UserUpdate(BaseModel):
  full_name: str
  role: USER_ROLE
  password: str
  is_active: int
  class Config:
    use_enum_values = True
