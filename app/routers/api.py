from fastapi import APIRouter
from app.routers import (
    users,
    auth,
    customers,
    device,
    device_category,
    device_borrowing,
    maintenance_services,
)

router = APIRouter()


def include_api_routes():
    router.include_router(maintenance_services.router)
    router.include_router(device_borrowing.router)
    router.include_router(device_category.router)
    router.include_router(device.router)
    router.include_router(customers.router)
    router.include_router(users.router)
    router.include_router(auth.router)


include_api_routes()
