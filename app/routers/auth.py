from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.core.dependencies import get_db
from app.services.auth.authorize import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_current_active_user,
)
from app.services.auth.authorize_schema import Token, UserLogin
from app.services.customer.customer_service import CustomerService
from app.services.device_borrowing.device_borrowing_service import (
    DeviceBorrowingService,
)
from app.services.device_category.device_category_service import DeviceCategoryService
from app.services.device_repairs.device_repairs_service import DeviceRepairsService
from app.services.devices.device_service import DeviceService
from app.services.maintenance_services.maintenance_services_service import (
    MaintenanceServicesService,
)
from app.services.notifies.notifies_service import NotifyService
from app.services.room_bookings.room_booking_service import RoomBookingService
from app.services.rooms.room_service import RoomService
from app.services.users.user_schema import UserBase
from sqlalchemy.orm import Session

from app.services.users.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(body: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, body.email, body.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserBase)
async def me(current_user: Annotated[UserBase, Depends(get_current_active_user)]):
    return current_user


@router.get("/reload-db")
async def reload_db(db: Session = Depends(get_db)):
    customer_service = CustomerService()
    user_service = UserService()
    device_borrowing_service = DeviceBorrowingService()
    device_category = DeviceCategoryService()
    device_repair = DeviceRepairsService()
    device = DeviceService()
    maintenance_services = MaintenanceServicesService()
    notification = NotifyService()
    room_booking = RoomBookingService()
    room_service = RoomService()

    run_success = 0
    die_service = []

    try:
        customer_service.get_all_users(db)
        run_success = run_success + 1
    except Exception as e:
        die_service.append("customer_service")

    try:
        user_service.get_all_users(db)
        run_success = run_success + 1
    except Exception as e:
        die_service.append("user_service")

    try:
        device_borrowing_service.get_all_device_borrowing(db)
        run_success = run_success + 1
    except Exception as e:
        die_service.append("device_borrowing_service")

    try:
        device_category.get_all_category(db)
        run_success = run_success + 1
    except Exception as e:
        die_service.append("device_category")

    try:
        device_repair.get_all_device_repairs(db)
        run_success = run_success + 1
    except Exception as e:
        die_service.append("device_repair")

    try:
        device.get_devices(db)
        run_success = run_success + 1
    except Exception as e:
        die_service.append("device")

    try:
        maintenance_services.get_all_services(db)
        run_success = run_success + 1
    except Exception as e:
        die_service.append("maintenance_services")

    try:
        notification.get_notifies(db)
        run_success = run_success + 1
    except Exception as e:
        die_service.append("notification")

    try:
        room_booking.get_all_room_bookings(db)
        run_success = run_success + 1
    except Exception as e:
        die_service.append("room_booking")

    try:
        room_service.get_all_rooms(db)
        run_success = run_success + 1
    except Exception as e:
        die_service.append("room_service")

    return JSONResponse(
        content={
            "message": f"Run success {run_success}/10 services",
            "die_service": die_service,
        }
    )
