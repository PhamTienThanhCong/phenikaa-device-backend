from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from app.core.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, index=True)
    full_name = Column(String(100), index=True)
    avatar = Column(String(100), index=True, default="default.jpg")
    birth_date = Column(String(20), index=True)
    gender = Column(Integer, index=True)
    address = Column(String(100), index=True)
    phone_number = Column(String(20), index=True)
    card_id = Column(String(20), index=True)

    __table_args__ = {"mysql_collate": "utf8mb4_unicode_ci"}
