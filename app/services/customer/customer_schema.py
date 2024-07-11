
from pydantic import BaseModel, EmailStr

from app.enums.customer_role import CUSTOMER_ROLE, CUSTOMER_STATUS

class CustomerUpdate(BaseModel):
  full_name: str
  avatar: str | None
  birth_date: str | None
  gender: int | None
  address: str | None
  phone_number: str | None
  card_id: str | None
  date_start: str | None
  expired: int | None
  department: str | None
  status: CUSTOMER_STATUS | None

  class Config:
    use_enum_values = True


class CustomerBase(BaseModel):
  id: int
  role: CUSTOMER_ROLE
  email: EmailStr | str
  full_name: str
  avatar: str | None
  birth_date: str | None
  gender: int | None
  address: str | None
  phone_number: str | None
  card_id: str | None
  date_start: str | None
  expired: int | None
  department: str | None
  status: CUSTOMER_STATUS | None

  class Config:
    use_enum_values = True
