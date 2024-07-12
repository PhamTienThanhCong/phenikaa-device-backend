from typing import Any
from app.services.profile.profile_schema import ProfileCreate
from app.services.profile.profile_model import Profile
from sqlalchemy.orm import Session

class ProfileService:
  def __init__(self):
    pass

  def get_profile(self, db:Session ,user_id: int):
    return db.query(Profile).filter(Profile.user_id == user_id).first()
  
  def create_profile(self, db:Session, profile: ProfileCreate, user_id: int):
    db_profile = Profile(**profile.dict(), user_id=user_id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile
  
  def update_profile(self, db:Session, profile: ProfileCreate, user_id:int):
    user_profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not user_profile:
      return None
    
    for key, value in profile.dict().items():
      setattr(user_profile, key, value)
    db.commit()
    db.refresh(user_profile)

    return user_profile
  
  def get_profile_by_users_id(self, db:Session, user_id: list[int]):
    return db.query(Profile).filter(Profile.user_id.in_(user_id)).all()
  
  def delete_profile(self, db:Session, user_id:int):
    user_profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not user_profile:
      return None
    db.delete(user_profile)
    db.commit()
    return user_profile