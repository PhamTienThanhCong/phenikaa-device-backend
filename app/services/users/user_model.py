from sqlalchemy import Boolean, Column, Integer, String
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(50))
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(50))
    role = Column(Integer)
    is_active = Column(Boolean, default=True)