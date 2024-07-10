from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.authorize import get_password_hash
from app.services.users.user_schema import UserCreate
from app.services.users.user_model import User

class UserService:
  def __init__(self):
    pass
  
  def get_user_by_email(self, db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

  def create_user(self, db: Session, user: UserCreate):
    # hash password
    user.password = get_password_hash(user.password)
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
  
  def get_all_users(self, db: Session):
    return db.query(User).all()
  
  def get_user_by_id(self, db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
  
  def update_user(self, db: Session, user_id: int, user: UserCreate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
      raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict().items():
      setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user
    
  def delete_user(self, db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
      raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user  
  