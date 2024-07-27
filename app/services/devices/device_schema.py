from pydantic import BaseModel


class DeviceCoreSchema(BaseModel):
    id: int
    name: str
    category: str
    information: str
    note: str
    total: int
    image: str
    total_used: int
    total_maintenance: int
    is_active: int


class DeviceCreateSchema(BaseModel):
    name: str
    category: str
    information: str | None
    image: str | None = "default.jpg"
    note: str | None
    total: int


class DeviceCreateSchemaFull(DeviceCreateSchema):
    presigned_url: str | None


class DeviceCreateResponse(DeviceCoreSchema):
    presigned_url: str | None


class DeviceUpdateResponse(DeviceCoreSchema):
    presigned_url: str | None


class DeviceUpdateSchema(BaseModel):
    name: str | None
    category: str | None
    information: str | None
    note: str | None
    image: str | None
    total: int | None
    total_used: int | None
    total_maintenance: int | None
    is_active: bool | None


class DeviceUpdateSchemaFull(DeviceUpdateSchema):
    presigned_url: str | None
