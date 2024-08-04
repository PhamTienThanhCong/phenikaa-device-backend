from pydantic import BaseModel, EmailStr

from app.enums.user_role import USER_ROLE
from app.services.profile.profile_schema import ProfileBase, ProfileCreate


class UserBase(BaseModel):
    id: int
    full_name: str
    email: EmailStr | str
    role: USER_ROLE
    is_active: int
    profile: ProfileBase | None = None

    class Config:
        use_enum_values = True


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    role: USER_ROLE
    password: str
    profile: ProfileCreate

    class Config:
        use_enum_values = True


class UserUpdate(BaseModel):
    full_name: str
    role: USER_ROLE
    password: str
    is_active: int
    profile: ProfileCreate

    class Config:
        use_enum_values = True
