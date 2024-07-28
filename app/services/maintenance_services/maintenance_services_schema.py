from pydantic import BaseModel, EmailStr


class MaintenanceServicePayload(BaseModel):
    guardian: str
    name: str
    description: str | None
    address: str | None
    phone: str
    email: EmailStr
    status: bool
    map_url: str | None


class MaintenanceServiceBase(MaintenanceServicePayload):
    id: int
