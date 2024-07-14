from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from app.core.database import Base

class Device(Base):
  __tablename__ = "devices"

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(100), index=True)
  category = Column(String(100), index=True)
  image = Column(String(255), default="default.jpg")
  presigned_url = Column(String(255), default="")
  information = Column(String(255), index=True, default="")
  note = Column(String(255), index=True, default="")
  total = Column(Integer, default=0)
  total_used = Column(Integer, default=0)
  total_maintenance = Column(Integer, default=0)
  is_active = Column(Boolean, default=True)