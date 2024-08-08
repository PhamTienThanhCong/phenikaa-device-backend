from sqlalchemy import Boolean, Column, Integer, String
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(50))
    email = Column(String(50), unique=True, index=True)
    password = Column(String(250))
    role = Column(Integer, default=1)
    is_active = Column(Integer, default=0)

    __table_args__ = {"mysql_collate": "utf8mb4_unicode_ci"}
