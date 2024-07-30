from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile

from app.core.dependencies import get_db
from sqlalchemy.orm import Session

from app.services.auth.authorize import get_current_active_user
from app.services.notifies.notifies_schema import (
    NotifySchemaBase,
    NotifySchemaCreate,
    NotifySchemaUpdate,
)
from app.services.notifies.notifies_service import NotifyService
from app.services.users.user_schema import UserBase

router = APIRouter(prefix="/notify", tags=["Notifies"])

notify_service = NotifyService()


@router.get("/", response_model=List[NotifySchemaBase])
async def get_notifies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return notify_service.get_notifies(db, skip, limit)


@router.get("/{notify_id}", response_model=NotifySchemaBase)
async def get_notify_by_id(notify_id: int, db: Session = Depends(get_db)):
    return notify_service.get_notify_by_id(db, notify_id)


@router.post("/", response_model=str)
async def create_notify(
    notify: NotifySchemaCreate,
    db: Session = Depends(get_db),
):
    return notify_service.create_notify(db, notify)


@router.put("/{notify_id}/readd", response_model=NotifySchemaBase)
async def make_read_notify(
    current_user: Annotated[UserBase, Depends(get_current_active_user)],
    explain_data: NotifySchemaUpdate,
    notify_id: int,
    db: Session = Depends(get_db),
):
    return notify_service.make_read_notify(db, notify_id, explain_data, current_user.id)


# @router.delete("/{notify_id}")
# async def delete_notify(notify_id: int, db: Session = Depends(get_db)):
#     return notify_service.delete_notify(db, notify_id)
