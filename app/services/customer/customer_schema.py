from pydantic import BaseModel, EmailStr

from app.enums.customer_role import CUSTOMER_ROLE, CUSTOMER_STATUS


class CustomerUpdate(BaseModel):
    full_name: str
    avatar: str | None = None
    birth_date: str | None = None
    gender: int | None = None
    address: str | None = None
    phone_number: str | None = None
    card_id: str | None = None
    date_start: str | None = None
    expired: int | None = None
    department: str | None = None
    status: CUSTOMER_STATUS | None = None

    class Config:
        use_enum_values = True


class CustomerBase(BaseModel):
    id: int
    role: CUSTOMER_ROLE
    email: EmailStr | str
    full_name: str
    avatar: str | None = None
    birth_date: str | None = None
    gender: int | None = None
    address: str | None = None
    phone_number: str | None = None
    card_id: str | None = None
    date_start: str | None = None
    expired: int | None = None
    department: str | None = None
    status: CUSTOMER_STATUS | None = None

    class Config:
        use_enum_values = True
