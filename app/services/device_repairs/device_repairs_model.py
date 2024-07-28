from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, String
from app.core.database import Base


class DeviceRepairs(Base):
    __tablename__ = "device_repairs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    is_returned = Column(Boolean, default=False)
    devices = Column(JSON)
    user_id = Column(Integer)
    service_id = Column(Integer)
    returning_date = Column(DateTime)
    retired_date = Column(DateTime, nullable=True, default=None)
    note = Column(String(255))
    created_at = Column(DateTime)
