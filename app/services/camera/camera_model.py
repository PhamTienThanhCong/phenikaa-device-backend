from sqlalchemy import Boolean, Column, Integer, String
from app.core.database import Base


class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    location_code = Column(String(255))
    location = Column(String(255))
    status = Column(Integer, default=1)
    stream_url = Column(String(255))

    __table_args__ = {"mysql_collate": "utf8mb4_unicode_ci"}
