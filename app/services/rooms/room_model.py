from sqlalchemy import JSON, Boolean, Column, ForeignKey, Integer, String
from app.core.database import Base


class Room(Base):
    __tablename__ = "rooms"

    room_id = Column(String(30), primary_key=True)
    category = Column(String(100))
    house_name = Column(String(20))
    manager = Column(String(100))
    detail = Column(JSON, default={})
    note = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_using = Column(Boolean, default=False)
    is_maintenance = Column(Boolean, default=False)

    __table_args__ = {"mysql_collate": "utf8mb4_unicode_ci"}
