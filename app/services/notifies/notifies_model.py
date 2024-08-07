from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, String
from app.core.database import Base


class Notify(Base):
    __tablename__ = "notifies"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer)
    title = Column(String(255))
    category = Column(String(255), index=True, default="system")
    content = Column(String(255))
    explain = Column(String(255), nullable=True, default=None)
    is_read = Column(Boolean, default=False)
    is_cancel = Column(Boolean, default=False)
    created_at = Column(DateTime)
    confirmed_at = Column(DateTime, nullable=True, default=None)
    user_id = Column(Integer, nullable=True, default=None)
    location_info = Column(JSON, nullable=True, default=None)
