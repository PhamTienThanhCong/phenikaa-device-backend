from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_db
from app.services.auth.authorize import get_current_active_user
from app.services.customer.customer_schema import CustomerBase, CustomerUpdate
from app.services.customer.customer_service import CustomerService
from sqlalchemy.orm import Session

from app.services.users.user_schema import UserBase

router = APIRouter(prefix="/customer", tags=["customers"])

customer_service = CustomerService()


@router.get("/health", response_model=str)
def health():
    return customer_service.get_health()


# get all users
@router.get("/", response_model=list[CustomerBase])
def get_all_users(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    return customer_service.get_all_users(db, limit, offset)


# get user by id
@router.get("/{id}", response_model=CustomerBase)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = customer_service.get_user_by_id(db, id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# create new user
@router.post("/", response_model=CustomerBase)
def create_user(user: CustomerBase, db: Session = Depends(get_db)):
    if customer_service.get_user_by_id(db, user.id):
        raise HTTPException(status_code=400, detail="User already exists")
    return customer_service.create_user(db, user)


# update user
@router.put("/{id}", response_model=CustomerBase)
def update_user(
    current_user: Annotated[UserBase, Depends(get_current_active_user)],
    id: int,
    user: CustomerUpdate,
    db: Session = Depends(get_db),
):
    if not customer_service.get_user_by_id(db, id):
        raise HTTPException(status_code=404, detail="User not found")
    return customer_service.update_user(db, user, id)


# delete user
@router.delete("/{id}", response_model=int)
def delete_user(
    current_user: Annotated[UserBase, Depends(get_current_active_user)],
    id: int,
    db: Session = Depends(get_db),
):
    if not customer_service.get_user_by_id(db, id):
        raise HTTPException(status_code=404, detail="User not found")
    return customer_service.delete_user(db, id)
