from sqlalchemy import Boolean, Column, Integer, String
from app.core.database import Base


class MaintenanceServices(Base):
    __tablename__ = "maintenance_services"

    id = Column(Integer, primary_key=True)
    guardian = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    status = Column(Boolean, default=True)
    map_url = Column(String(255), nullable=True)

    __table_args__ = {"mysql_collate": "utf8mb4_unicode_ci"}
