from pydantic import BaseModel, EmailStr


class MaintenanceServicePayload(BaseModel):
    guardian: str
    name: str
    description: str | None = None
    address: str | None = None
    phone: str
    email: EmailStr
    status: bool
    map_url: str | None = None


class MaintenanceServiceBase(MaintenanceServicePayload):
    id: int
