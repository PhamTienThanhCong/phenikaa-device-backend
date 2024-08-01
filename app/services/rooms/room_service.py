import json
from typing import Any, List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.services.rooms.room_model import Room
from app.services.rooms.room_schema import (
    RoomSchemaBase,
    RoomSchemaCreate,
    RoomSchemaUpdate,
)


class RoomService:
    def __init__(self):
        pass

    def get_rooms_by_ids(
        self, db: Session, room_ids: List[str]
    ) -> List[RoomSchemaBase]:
        rooms = db.query(Room).filter(Room.room_id.in_(room_ids)).all()
        for room in rooms:
            room.detail = json.loads(room.detail)
        return rooms

    def using_room(self, db: Session, room_id: str, is_using: bool = True) -> str:
        room = self.get_room_by_id(db, room_id)
        if not room:
            raise HTTPException(status_code=400, detail="Room not found")
        if room.is_active == False:
            raise HTTPException(status_code=400, detail="Room is not active")
        if room.is_maintenance == True:
            raise HTTPException(status_code=400, detail="Room is in maintenance")
        room.is_using = is_using
        db.query(Room).filter(Room.room_id == room_id).update(room.dict())
        db.commit()
        return True

    def get_all_rooms(self, db: Session) -> List[RoomSchemaBase]:
        # get all rooms
        rooms = db.query(Room).all()
        for room in rooms:
            room.detail = json.loads(room.detail)
        return rooms

    def get_room_by_id(self, db: Session, room_id: str, load=True) -> RoomSchemaBase:
        # get room by id
        room_id = room_id.upper()
        room = db.query(Room).filter(Room.room_id == room_id).first()
        if room and load == True:
            room.detail = json.loads(room.detail)
        return room

    def create_room(self, db: Session, room: RoomSchemaCreate) -> RoomSchemaBase:
        data_room = room.dict()
        data_room["room_id"] = data_room["room_id"].upper()
        data_room["house_name"] = data_room["house_name"].upper()
        if self.get_room_by_id(db, data_room["room_id"]):
            raise HTTPException(status_code=400, detail="Room already exists")
        data_room["detail"] = json.dumps(data_room["detail"])
        # save to database
        db_room = Room(**data_room)
        db.add(db_room)
        db.commit()

        return self.get_room_by_id(db, data_room["room_id"])

    def update_room(
        self, db: Session, room_id: str, room: RoomSchemaUpdate
    ) -> RoomSchemaBase:
        data_room = room.dict()
        room_id = room_id.upper()
        data_room["house_name"] = data_room["house_name"].upper()
        data_room["detail"] = json.dumps(data_room["detail"])
        # update to database
        db.query(Room).filter(Room.room_id == room_id).update(data_room)
        db.commit()

        return self.get_room_by_id(db, room_id)

    def delete_room(self, db: Session, room_id: str) -> str:
        room_id = room_id.upper()
        # delete room by id
        room_id = room_id.upper()
        db.query(Room).filter(Room.room_id == room_id).delete()
        db.commit()
        return "ok"
