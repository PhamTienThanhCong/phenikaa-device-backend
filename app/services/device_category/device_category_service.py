import uuid
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.core.setting import get_setting
from app.services.device_category.device_category_model import DeviceCategory
from app.services.device_category.device_category_schema import DeviceCategorySchema
from app.services.devices.device_service import DeviceService
from app.utils.save_file import save_file_image


class DeviceCategoryService:
    def __init__(self):
        self.base = get_setting()
        self.device_service = DeviceService()
        pass

    def get_all_category(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> list[DeviceCategorySchema]:
        categories = db.query(DeviceCategory).offset(skip).limit(limit).all()
        # get all name of category
        category_names = [category.name for category in categories]
        # get total devices of each category
        total_devices = self.device_service.count_devices(db, category_names)

        for category in categories:
            if category.name in total_devices:
                category.total_devices = total_devices[category.name]
            else:
                category.total_devices = (
                    0  # nếu không tìm thấy, đặt giá trị mặc định là 0
                )
            if category.presigned_url:
                category.presigned_url = f"{self.base['base_url']}/v1/device-category/{category.presigned_url}"
            else:
                category.presigned_url = ""

        return categories

    def get_category_by_name(self, db: Session, category_name: str):
        category = (
            db.query(DeviceCategory)
            .filter(DeviceCategory.name == category_name)
            .first()
        )
        return category

    def get_category_by_id(self, db: Session, category_id: int) -> DeviceCategorySchema:
        category = (
            db.query(DeviceCategory).filter(DeviceCategory.id == category_id).first()
        )
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        total_devices = self.device_service.count_devices(db, [category.name])

        if category.name in total_devices:
            category.total_devices = total_devices[category.name]
        else:
            category.total_devices = 0  # nếu không tìm thấy, đặt giá trị mặc định là 0
        if category.presigned_url:
            category.presigned_url = (
                f"{self.base['base_url']}/v1/device-category/{category.presigned_url}"
            )
        else:
            category.presigned_url = ""
        return category

    def create_category(
        self, db: Session, category: DeviceCategorySchema
    ) -> DeviceCategorySchema:
        if category.image:
            category.image = "/public/device-category/default.jpg"
            presigned_url = str(uuid.uuid4())
            db_category = DeviceCategory(**category.dict(), presigned_url=presigned_url)
        else:
            category.image = "/public/device-category/default.jpg"
            db_category = DeviceCategory(**category.dict())

        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return self.get_category_by_id(db, db_category.id)

    def update_category(
        self, db: Session, category_id: int, category: DeviceCategorySchema
    ) -> DeviceCategorySchema:
        update_data = category.dict()

        if category.image:
            presigned_url = str(uuid.uuid4())
            update_data["presigned_url"] = presigned_url

        del update_data["image"]
        db.query(DeviceCategory).filter(DeviceCategory.id == category_id).update(
            update_data
        )

        db.commit()

        return self.get_category_by_id(db, category_id)

    def upload_image(self, db: Session, presigned_url_id: str, file: UploadFile):

        device = (
            db.query(DeviceCategory)
            .filter(DeviceCategory.presigned_url == presigned_url_id)
            .first()
        )
        if device is None:
            raise HTTPException(status_code=404, detail="Device not found")

        file_path = f"/public/device-category/device-category-{device.id}.jpg"

        # update image path to device
        save_file_image(file, file_path)

        db.query(DeviceCategory).filter(DeviceCategory.id == device.id).update(
            {"image": file_path, "presigned_url": ""}
        )
        db.commit()
        return {"message": "Image uploaded successfully"}
