import datetime
from typing import Any, List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.services.customer.customer_service import CustomerService
from app.services.room_bookings.room_booking_model import RoomBooking
from app.services.room_bookings.room_booking_schema import (
    RoomBookingSchemaBase,
    RoomBookingSchemaCreate,
    RoomBookingSchemaUpdate,
)
from app.services.rooms.room_service import RoomService
from app.services.users.user_service import UserService


class RoomBookingService:
    def __init__(self):
        self.user = UserService()
        self.customer = CustomerService()
        self.room = RoomService()

    def validate_room(
        self,
        db: Session,
        room_id: str,
        date_booking: str,
        start_time: str,
        end_time: str,
        room_booking_id: int = 0,
    ):
        # Chuyển đổi date_booking, start_time và end_time từ str sang đối tượng datetime
        date_booking = datetime.datetime.strptime(date_booking, "%Y-%m-%d").date()
        start_time = datetime.datetime.strptime(start_time, "%H:%M:%S").time()
        end_time = datetime.datetime.strptime(end_time, "%H:%M:%S").time()

        room = self.room.get_room_by_id(db, room_id, False)
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")

        if room_booking_id != 0:
            room_bookings = (
                db.query(RoomBooking)
                .filter(RoomBooking.room_id == room_id)
                .filter(RoomBooking.date_booking == date_booking)
                .all()
            )
        else:
            room_bookings = (
                db.query(RoomBooking)
                .filter(RoomBooking.room_id == room_id)
                .filter(RoomBooking.date_booking == date_booking)
                .filter(RoomBooking.id != room_booking_id)
                .all()
            )

        for room_booking in room_bookings:
            # Kiểm tra xem thời gian bắt đầu và kết thúc của booking mới có nằm trong khoảng thời gian của booking cũ không
            if (
                room_booking.start_time <= start_time < room_booking.end_time
                or room_booking.start_time < end_time <= room_booking.end_time
            ):
                raise HTTPException(
                    status_code=400,
                    detail="Room is already booked in this time. Please choose another time",
                )

    def get_room_status(self, room_booking):
        current_time = datetime.datetime.now()

        # Tạo các đối tượng datetime từ thông tin booking
        booking_date = room_booking.date_booking
        booking_start = datetime.datetime.combine(booking_date, room_booking.start_time)
        booking_end = datetime.datetime.combine(booking_date, room_booking.end_time)

        if current_time < booking_start:
            return "đang chờ"
        elif booking_start <= current_time < booking_end:
            return "đang sử dụng"
        else:
            return "đã sử dụng"

    def get_all_room_bookings(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[RoomBookingSchemaBase]:
        room_bookings = (
            db.query(RoomBooking)
            .order_by(RoomBooking.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        user_ids = [room_booking.user_id for room_booking in room_bookings]
        customer_ids = [room_booking.customer_id for room_booking in room_bookings]
        room_ids = [room_booking.room_id for room_booking in room_bookings]
        users = self.user.get_users_by_ids(db, user_ids)
        customers = self.customer.get_customer_by_ids(db, customer_ids)
        rooms = self.room.get_rooms_by_ids(db, room_ids)
        for room_booking in room_bookings:
            for user in users:
                if room_booking.user_id == user.id:
                    room_booking.user = user
                    break
            for customer in customers:
                if room_booking.customer_id == customer.id:
                    room_booking.customer = customer
                    break
            for room in rooms:
                if room_booking.room_id == room.room_id:
                    room_booking.room = room
                    break

            room_booking.status = self.get_room_status(room_booking)

        return room_bookings

    def get_room_booking_by_id(
        self, db: Session, room_booking_id: int
    ) -> RoomBookingSchemaBase:
        room_booking = (
            db.query(RoomBooking).filter(RoomBooking.id == room_booking_id).first()
        )
        if not room_booking:
            raise HTTPException(status_code=404, detail="Room booking not found")
        user = self.user.get_user_by_id(db, room_booking.user_id)
        customer = self.customer.get_user_by_id(db, room_booking.customer_id)
        room = self.room.get_room_by_id(db, room_booking.room_id)
        room_booking.user = user
        room_booking.customer = customer
        room_booking.room = room
        room_booking.status = self.get_room_status(room_booking)
        return room_booking

    def create_room_booking(
        self, db: Session, room_booking: RoomBookingSchemaCreate
    ) -> RoomBookingSchemaBase:
        data = room_booking.dict()
        self.user.validate_user(db, data.get("user_id"))
        self.customer.validate_customer(db, data.get("customer_id"))
        self.validate_room(
            db,
            data.get("room_id"),
            data.get("date_booking"),
            data.get("start_time"),
            data.get("end_time"),
        )
        created_at = datetime.datetime.now()
        data["created_at"] = created_at
        data["updated_at"] = created_at

        db_room_booking = RoomBooking(**data)
        db.add(db_room_booking)
        db.commit()
        return self.get_room_booking_by_id(db, db_room_booking.id)

    def update_room_booking(
        self, db: Session, room_booking_id: int, room_booking: RoomBookingSchemaUpdate
    ) -> RoomBookingSchemaBase:
        data = room_booking.dict()
        self.validate_room(
            db,
            data.get("room_id"),
            data.get("date_booking"),
            data.get("start_time"),
            data.get("end_time"),
            room_booking_id,
        )
        data["updated_at"] = datetime.datetime.now()
        db.query(RoomBooking).filter(RoomBooking.id == room_booking_id).update(data)
        db.commit()
        return self.get_room_booking_by_id(db, room_booking_id)

    def delete_room_booking(self, db: Session, room_booking_id: int) -> str:
        db.query(RoomBooking).filter(RoomBooking.id == room_booking_id).delete()
        db.commit()
        return "ok"
