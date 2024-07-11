
from pydantic import BaseModel

class ProfileBase(BaseModel):
  id: int 
  user_id: int | None
  full_name: str
  avatar: str
  birth_date: str = None
  gender: int = None
  address: str = None
  phone_number: str = None
  card_id: str = None

class ProfileCreate(BaseModel):
  full_name: str | None
  avatar: str | None
  birth_date: str | None
  gender: int | None
  address: str | None
  phone_number: str | None
  card_id: str | None
