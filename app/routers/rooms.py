from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, UploadFile

from app.core.dependencies import get_db
from sqlalchemy.orm import Session

from app.services.auth.authorize import get_current_active_user
from app.services.rooms.room_schema import (
    RoomSchemaBase,
    RoomSchemaCreate,
    RoomSchemaUpdate,
)
from app.services.rooms.room_service import RoomService


router = APIRouter(prefix="/room", tags=["room"])

device_service = RoomService()


@router.get("", response_model=list[RoomSchemaBase])
def get_all_rooms(db: Session = Depends(get_db)):
    rooms = device_service.get_all_rooms(db)
    return rooms


@router.get("/{room_id}", response_model=RoomSchemaBase)
def get_room_by_id(room_id: str, db: Session = Depends(get_db)):
    room = device_service.get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


@router.post("")
def create_room(room: RoomSchemaCreate, db: Session = Depends(get_db)):
    return device_service.create_room(db, room)


@router.put("/{room_id}", response_model=RoomSchemaBase)
def update_room(room_id: str, room: RoomSchemaUpdate, db: Session = Depends(get_db)):
    _room = device_service.get_room_by_id(db, room_id)
    if not _room:
        raise HTTPException(status_code=404, detail="Room not found")
    return device_service.update_room(db, room_id, room)


@router.delete("/{room_id}", response_model=str)
def delete_room(room_id: str, db: Session = Depends(get_db)):
    _room = device_service.get_room_by_id(db, room_id)
    if not _room:
        raise HTTPException(status_code=404, detail="Room not found")
    return device_service.delete_room(db, room_id)
