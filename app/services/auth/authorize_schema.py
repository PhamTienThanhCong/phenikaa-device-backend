from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int

class UserLogin(BaseModel):
  email: EmailStr
  password: str