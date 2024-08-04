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
    information: str | None = None
    image: str | None = "default.jpg"
    note: str | None = None
    total: int


class DeviceCreateSchemaFull(DeviceCreateSchema):
    presigned_url: str | None = None


class DeviceCreateResponse(DeviceCoreSchema):
    presigned_url: str | None = None


class DeviceUpdateResponse(DeviceCoreSchema):
    presigned_url: str | None = None


class DeviceUpdateSchema(BaseModel):
    name: str | None = None
    category: str | None = None
    information: str | None = None
    note: str | None = None
    image: str | None = None
    total: int | None = None
    total_used: int | None = None
    total_maintenance: int | None = None
    is_active: bool | None = None


class DeviceUpdateSchemaFull(DeviceUpdateSchema):
    presigned_url: str | None
