from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from app.core.database import Base


class DeviceCategory(Base):
    __tablename__ = "device_category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), index=True)
    is_active = Column(Boolean, default=True)
    image = Column(String(255), default="default.jpg")
    presigned_url = Column(String(255), default="")

    __table_args__ = {"mysql_collate": "utf8mb4_unicode_ci"}
