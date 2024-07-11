from sqlalchemy import Boolean, Column, Integer, String
from app.core.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    role = Column(Integer, index=True)
    email = Column(String(100), index=True)
    full_name = Column(String(100), index=True)
    avatar = Column(String(100), index=True, default="default.jpg")
    birth_date = Column(String(20), index=True)
    gender = Column(Integer, index=True)
    address = Column(String(100), index=True)
    phone_number = Column(String(20), index=True)
    card_id = Column(String(20), index=True)
    date_start = Column(String(20), index=True)
    expired = Column(Boolean, default=False)
    department = Column(String(100), index=True)
    status = Column(Integer, index=True)