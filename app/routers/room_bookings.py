from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile

from app.core.dependencies import get_db
from sqlalchemy.orm import Session

from app.services.auth.authorize import get_current_active_user
from app.services.room_bookings.room_booking_schema import (
    RoomBookingSchemaBase,
    RoomBookingSchemaCreate,
    RoomBookingSchemaUpdate,
)
from app.services.room_bookings.room_booking_service import RoomBookingService

from app.services.rooms.room_service import RoomService

router = APIRouter(prefix="/room-booking", tags=["room booking"])

room_booking_service = RoomBookingService()


@router.get("/", response_model=list[RoomBookingSchemaBase])
def get_all_room_bookings(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    room_bookings = room_booking_service.get_all_room_bookings(db, skip, limit)
    return room_bookings


@router.get("/{room_booking_id}", response_model=RoomBookingSchemaBase)
def get_room_booking_by_id(room_booking_id: int, db: Session = Depends(get_db)):
    room_booking = room_booking_service.get_room_booking_by_id(db, room_booking_id)
    if not room_booking:
        raise HTTPException(status_code=404, detail="Room booking not found")
    return room_booking


@router.post("/", response_model=RoomBookingSchemaBase)
def create_room_booking(
    room_booking: RoomBookingSchemaCreate, db: Session = Depends(get_db)
):
    return room_booking_service.create_room_booking(db, room_booking)


@router.put("/{room_booking_id}", response_model=RoomBookingSchemaBase)
def update_room_booking(
    room_booking_id: int,
    room_booking: RoomBookingSchemaUpdate,
    db: Session = Depends(get_db),
):
    _room_booking = room_booking_service.get_room_booking_by_id(db, room_booking_id)
    if not _room_booking:
        raise HTTPException(status_code=404, detail="Room booking not found")
    return room_booking_service.update_room_booking(db, room_booking_id, room_booking)


@router.delete("/{room_booking_id}", response_model=str)
def delete_room_booking(room_booking_id: int, db: Session = Depends(get_db)):
    _room_booking = room_booking_service.get_room_booking_by_id(db, room_booking_id)
    if not _room_booking:
        raise HTTPException(status_code=404, detail="Room booking not found")
    return room_booking_service.delete_room_booking(db, room_booking_id)
