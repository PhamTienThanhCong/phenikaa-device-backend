from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.services.customer.customer_schema import CustomerBase, CustomerUpdate
from app.services.customer.customer_model import Customer
from app.services.maintenance_services.maintenance_services_model import (
    MaintenanceServices,
)


class MaintenanceServicesService:
    def __init__(self):
        pass

    def get_health(self):
        return "OK"

    def get_all_services(self, db: Session, skip: int = 0, limit: int = 100):
        services = db.query(MaintenanceServices).offset(skip).limit(limit).all()
        return services

    def get_services_by_ids(self, db: Session, service_ids: list[int]):
        services = (
            db.query(MaintenanceServices)
            .filter(MaintenanceServices.id.in_(service_ids))
            .all()
        )
        return services

    def validate_service(self, db: Session, service_id: int):
        service = self.get_service_by_id(db, service_id)
        if not service:
            raise JSONResponse(
                status_code=404, content={"message": "Service not found"}
            )
        return True

    def get_service_by_id(self, db: Session, service_id: int):
        service = (
            db.query(MaintenanceServices)
            .filter(MaintenanceServices.id == service_id)
            .first()
        )
        return service

    def create_service(self, db: Session, service: CustomerBase):
        # phone and email must be unique
        db_service = MaintenanceServices(**service.dict())
        db.add(db_service)
        db.commit()
        db.refresh(db_service)
        return db_service

    def update_service(self, db: Session, service_id: int, service: CustomerUpdate):
        db_service = (
            db.query(MaintenanceServices)
            .filter(MaintenanceServices.id == service_id)
            .first()
        )
        if db_service:
            for key, value in service.dict().items():
                setattr(db_service, key, value)
            db.commit()
            db.refresh(db_service)
            return db_service
        raise JSONResponse(status_code=404, content={"message": "Service not found"})

    def delete_service(self, db: Session, service_id: int):
        db_service = (
            db.query(MaintenanceServices)
            .filter(MaintenanceServices.id == service_id)
            .first()
        )
        if db_service:
            db.delete(db_service)
            db.commit()
            return "ok"
        raise JSONResponse(status_code=404, content={"message": "Service not found"})
