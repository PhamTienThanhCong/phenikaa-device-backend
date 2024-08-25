import random
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.services.camera.camera_model import Camera
from app.services.camera.camera_schema import (
    CameraCreateSchema,
    CameraSchema,
    CameraUpdateSchema,
)


class CameraService:
    def __init__(self):
        pass

    __example_camera = [
        "https://www.shutterstock.com/shutterstock/videos/1099731409/preview/stock-footage-view-from-security-cameras-in-business-center-woman-and-two-men-walk-in-corridor-workers-walking.webm4",
        "https://www.shutterstock.com/shutterstock/videos/1099731473/preview/stock-footage-view-from-cctv-camera-in-business-center-office-room-turning-on-the-light-in-modern-school-room-or.webm",
        "https://www.shutterstock.com/shutterstock/videos/1099731451/preview/stock-footage-view-from-cctv-cameras-at-flight-of-stairs-in-modern-business-center-colleagues-go-upstairs-to.webm",
        "https://www.shutterstock.com/shutterstock/videos/1099731483/preview/stock-footage-view-from-cctv-camera-in-business-center-office-room-turning-on-lights-in-modern-school-room-or.webm",
        "https://www.shutterstock.com/shutterstock/videos/3525668569/preview/stock-footage-aerial-view-of-people-inside-the-building-from-a-surveillance-camera.webm"
    ]

    def get_all(self, db: Session) -> CameraSchema:
        cameras = db.query(Camera).all()
        # change status
        for camera in cameras:
            camera.status = (
                "active"
                if camera.status == 1
                else "inactive" if camera.status == 0 else "deleted"
            )

        return cameras

    def get_by_id(self, db: Session, camera_id: int) -> CameraSchema:
        camera = db.query(Camera).filter(Camera.id == camera_id).first()
        if camera is None:
            raise HTTPException(status_code=404, detail="Camera not found")
        # change status
        camera.status = (
            "active"
            if camera.status == 1
            else "inactive" if camera.status == 0 else "deleted"
        )
        return camera

    def create(self, db: Session, camera: CameraCreateSchema) -> CameraSchema:
        data = camera.dict()
        if (data["stream_url"] is None) or (data["stream_url"] == ""):
            # ramdom stream_url
            index = random.randint(0, len(self.__example_camera) - 1)
            print(index)
            data["stream_url"] = self.__example_camera[index]
        camera = Camera(**data)
        db.add(camera)
        db.commit()

        # reload to get id
        db.refresh(camera)

        return self.get_by_id(db, camera.id)

    def update(
        self, db: Session, camera_id: int, camera: CameraUpdateSchema
    ) -> CameraSchema:
        data = camera.dict()
        camera = db.query(Camera).filter(Camera.id == camera_id).first()
        if camera is None:
            raise HTTPException(status_code=404, detail="Camera not found")

        for key, value in data.items():
            if value is not None and key != "id":
                setattr(camera, key, value)
        db.commit()

        return self.get_by_id(db, camera_id)

    def delete(self, db: Session, camera_id: int):
        camera = db.query(Camera).filter(Camera.id == camera_id).first()
        if camera is None:
            raise HTTPException(status_code=404, detail="Camera not found")
        db.delete(camera)
        db.commit()
        return "ok"
