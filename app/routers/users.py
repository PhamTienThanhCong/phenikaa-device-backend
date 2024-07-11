from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.services.auth.authorize import get_current_active_user
from app.services.users.user_schema import UserBase, UserCreate, UserUpdate
from app.services.users.user_service import UserService

router = APIRouter( 
  prefix="/user",
  tags=["users"]
)

user_service = UserService()

@router.get("/", response_model=list[UserBase])
def get_all_users(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
  return user_service.get_all_users(db, limit, offset)

@router.post("/", response_model=UserBase)
def create_user(body: UserCreate, db: Session = Depends(get_db)):
  # check if user already exists
  user = user_service.get_user_by_email(db, body.email)
  if user:
    raise HTTPException(status_code=400, detail="User already exists")
  return user_service.create_user(db, body)
  
@router.get("/{user_id}", response_model=UserBase)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
  user = user_service.get_user_by_id(db, user_id)
  if not user:
    raise HTTPException(status_code=404, detail="User not found")
  user.profile = user_service.profile.get_profile(db, user_id)
  return user

@router.put("/{user_id}", response_model=UserBase)
def update_user(user_id: int, body: UserUpdate, db: Session = Depends(get_db)):
  return user_service.update_user(db, user_id, body)

@router.delete("/{user_id}", response_model=str)
def delete_user(user_id: int, db: Session = Depends(get_db)):
  # if current_user.role != 1:
  #   raise HTTPException(status_code=401, detail="Unauthorized")
  return user_service.delete_user(db, user_id)