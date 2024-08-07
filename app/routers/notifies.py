from ast import parse
from typing import Annotated, List
from fastapi import APIRouter, Depends, Request


from app.core.dependencies import get_db
from sqlalchemy.orm import Session

from app.services.auth.authorize import get_current_active_user
from app.services.notifies.notifies_schema import (
    LocationInfo,
    NotifyCancelSchemaBase,
    NotifySchemaBase,
    NotifySchemaCreate,
    NotifySchemaUpdate,
)
from app.services.notifies.notifies_service import NotifyService
from app.services.users.user_schema import UserBase

router = APIRouter(prefix="/notify", tags=["Notifies"])

notify_service = NotifyService()


@router.get("/info", response_model=LocationInfo)
async def get_info(request: Request):
    client_ip = request.client.host
    user_agent_str = request.headers.get("user-agent")
    return await notify_service.get_my_ip(client_ip, user_agent_str)


@router.get("/", response_model=List[NotifySchemaBase])
async def get_notifies(
    skip: int = 0,
    limit: int = 100,
    category: str = "",
    customer_id: str = "",
    status: str = "",
    db: Session = Depends(get_db),
):
    return notify_service.get_notifies(db, skip, limit, category, customer_id, status)


@router.get("/{notify_id}", response_model=NotifySchemaBase)
async def get_notify_by_id(notify_id: int, db: Session = Depends(get_db)):
    return notify_service.get_notify_by_id(db, notify_id)


@router.post("/", response_model=NotifySchemaBase)
async def create_notify(
    notify: NotifySchemaCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    client_ip = request.client.host
    user_agent_str = request.headers.get("user-agent")
    return await notify_service.create_notify(db, notify, client_ip, user_agent_str)


@router.put("/{notify_id}/readd", response_model=NotifySchemaBase)
async def make_read_notify(
    current_user: Annotated[UserBase, Depends(get_current_active_user)],
    explain_data: NotifySchemaUpdate,
    notify_id: int,
    db: Session = Depends(get_db),
):
    return notify_service.make_read_notify(db, notify_id, explain_data, current_user.id)


@router.put("/{notify_id}/cancel", response_model=NotifySchemaBase)
async def make_read_notify(
    notify_cancel: NotifyCancelSchemaBase,
    notify_id: int,
    db: Session = Depends(get_db),
):
    return notify_service.cancel_notify(db, notify_id, notify_cancel)


# @router.delete("/{notify_id}")
# async def delete_notify(notify_id: int, db: Session = Depends(get_db)):
#     return notify_service.delete_notify(db, notify_id)
