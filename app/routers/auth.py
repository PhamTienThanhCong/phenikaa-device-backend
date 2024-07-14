from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.core.dependencies import get_db
from app.services.auth.authorize import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_active_user
from app.services.auth.authorize_schema import Token, UserLogin
from app.services.users.user_schema import UserBase
from sqlalchemy.orm import Session

router = APIRouter( 
  prefix="/auth",
  tags=["auth"]
)

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