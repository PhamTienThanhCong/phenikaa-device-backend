from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String, Date, Time
from app.core.database import Base


class RoomBooking(Base):
    __tablename__ = "room_bookings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), index=True)
    room_id = Column(String(30), index=True)
    user_id = Column(Integer)
    customer_id = Column(Integer)
    total_customer = Column(Integer, default=1)
    date_booking = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    note = Column(String(255), default="")
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    is_active = Column(Boolean, default=True)
