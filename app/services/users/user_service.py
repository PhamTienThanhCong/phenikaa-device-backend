from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.services.profile.profile_schema import ProfileCreate
from app.services.profile.profile_service import ProfileService
from app.services.users.user_schema import UserCreate
from app.services.users.user_model import User
from app.utils.hash_password import get_password_hash


class UserService:
    def __init__(self):
        self.profile = ProfileService()

    def get_user_by_email(self, db: Session, email: str):
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        profile = self.profile.get_profile(db, user.id)
        user.profile = profile
        return user

    def create_user(self, db: Session, user: UserCreate):
        # hash password
        user.password = get_password_hash(user.password)
        profile: ProfileCreate = user.profile
        del user.profile

        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        profile = self.profile.create_profile(db, profile, db_user.id)
        db_user.profile = profile
        return db_user

    def get_all_users(self, db: Session, limit: int, offset: int):
        user_list = db.query(User).limit(limit).offset(offset).all()
        # get id in user_list
        user_id_list = [user.id for user in user_list]

        # get profile by user_id
        profile_list = self.profile.get_profile_by_users_id(db, user_id_list)

        # map profile to user
        for user in user_list:
            for profile in profile_list:
                if user.id == profile.user_id:
                    user.profile = profile
                    break
        return user_list

    def get_users_by_ids(self, db: Session, user_ids: list[int]):
        user_list = db.query(User).filter(User.id.in_(user_ids)).all()
        # get profile by user_id
        for user in user_list:
            del user.password
            profile = self.profile.get_profile(db, user.id)
            user.profile = profile
        return user_list

    def get_user_by_id(self, db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        profile = self.profile.get_profile(db, user_id)
        user.profile = profile
        return user

    def update_user(self, db: Session, user_id: int, user: UserCreate):
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        profile: ProfileCreate = user.profile
        # remove profile from user
        del user.profile

        for key, value in user.dict().items():
            if key == "password":
                value = get_password_hash(value)
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)

        if profile:
            profile = self.profile.update_profile(db, profile, db_user.id)
            db_user.profile = profile

        return db_user

    def delete_user(self, db: Session, user_id: int):
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        self.profile.delete_profile(db, user_id)

        db.delete(db_user)
        db.commit()
        return JSONResponse(
            status_code=200, content={"message": "User deleted successfully"}
        )
