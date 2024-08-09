import asyncio
import datetime
import httpx
from user_agents import parse
from typing import Any, List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.services.customer.customer_service import CustomerService
from app.services.notifies.notifies_model import Notify
from app.services.notifies.notifies_schema import (
    LocationInfo,
    NotifyCancelSchemaBase,
    NotifySchemaBase,
    NotifySchemaCreate,
    NotifySchemaUpdate,
)
from app.services.users.user_service import UserService


class NotifyService:
    def __init__(self):
        self.customer = CustomerService()
        self.user = UserService()

    def get_test(self, db: Session) -> str:
        # get all notifies
        notifies = db.query(Notify).limit(10).all()
        return notifies

    async def get_my_ip(self, client_ip: str, user_agent_str: Any) -> LocationInfo:
        # Get location information using ipinfo.io
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://ipinfo.io/{client_ip}/json?token=7df94aa078031f"
            )
            location_data = response.json()

        # Get User-Agent header to determine device info
        user_agent = parse(user_agent_str)

        device_info = {
            "browser": user_agent.browser.family,
            "browser_version": user_agent.browser.version_string,
            "os": user_agent.os.family,
            "os_version": user_agent.os.version_string,
            "device": user_agent.device.family,
        }

        return {"ip": client_ip, "location": location_data, "device": device_info}

    def get_notifies(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        category: str = "",
        customer_id: str = "",
        status: str = "",
    ) -> List[NotifySchemaBase]:
        query = db.query(Notify)

        if category:
            query = query.filter(Notify.category.like(f"%{category}%"))

        if customer_id:
            query = query.filter(Notify.customer_id.like(f"%{customer_id}%"))

        notifies = query.order_by(Notify.created_at).offset(skip).limit(limit).all()

        user_ids = [notify.user_id for notify in notifies]
        customer_ids = [notify.customer_id for notify in notifies]

        customers = self.customer.get_customer_by_ids(db, customer_ids)
        users = self.user.get_users_by_ids(db, user_ids)
        for notify in notifies:
            for customer in customers:
                if notify.customer_id == customer.id:
                    notify.customer = customer
                    break
            for user in users:
                if notify.user_id == user.id:
                    notify.user_verifier = user
                    break
            if notify.user_id is None:
                notify.user_verifier = None
            if notify.is_cancel:
                status = "Đã hủy"
            else:
                status = (
                    "Đang chờ phản hồi" if notify.is_read is False else "Đã phản hồi"
                )
            notify.status = status
        return notifies

    def get_notify_by_id(self, db: Session, notify_id: int) -> NotifySchemaBase:
        notify = db.query(Notify).filter(Notify.id == notify_id).first()
        if notify is None:
            raise HTTPException(status_code=404, detail="Notify not found")
        user_ids = [notify.user_id]
        customer_ids = [notify.customer_id]

        customers = self.customer.get_customer_by_ids(db, customer_ids)
        users = self.user.get_users_by_ids(db, user_ids)
        for customer in customers:
            if notify.customer_id == customer.id:
                notify.customer = customer
                break
        for user in users:
            if notify.user_id == user.id:
                notify.user_verifier = user
                break
        if notify.user_id is None:
            notify.user_verifier = None

        if notify.is_cancel:
            status = "Đã hủy"
        else:
            status = "Đang chờ phản hồi" if notify.is_read is False else "Đã phản hồi"
        notify.status = status

        return notify

    async def create_notify(
        self,
        db: Session,
        notify: NotifySchemaCreate,
        client_ip: str,
        user_agent_str: str,
    ) -> NotifySchemaBase:
        data = notify.dict()
        user_ip = await self.get_my_ip(client_ip, user_agent_str)
        data["location_info"] = user_ip

        created_at = datetime.datetime.now()
        data["created_at"] = created_at
        self.customer.validate_customer(db, data["customer_id"])

        new_notify = Notify(**data)
        db.add(new_notify)
        db.commit()
        db.refresh(new_notify)
        return self.get_notify_by_id(db, new_notify.id)

    def make_read_notify(
        self,
        db: Session,
        notify_id: int,
        explain_data: NotifySchemaUpdate,
        user_id: int,
    ) -> NotifySchemaBase:
        notify = db.query(Notify).filter(Notify.id == notify_id).first()
        explain_data = explain_data.dict()
        notify.explain = explain_data["explain"]
        if notify is None:
            raise HTTPException(status_code=404, detail="Notify not found")

        if notify.is_cancel:
            raise HTTPException(status_code=400, detail="Notify has been canceled")

        notify.is_read = True
        notify.user_id = user_id
        notify.confirmed_at = datetime.datetime.now()
        db.commit()
        return self.get_notify_by_id(db, notify_id)

    def cancel_notify(
        self, db: Session, notify_id: int, notify_cancel: NotifyCancelSchemaBase
    ) -> NotifySchemaBase:
        notify = db.query(Notify).filter(Notify.id == notify_id).first()
        if notify is None:
            raise HTTPException(status_code=404, detail="Notify not found")

        if notify.customer_id != notify_cancel.customer_id:
            raise HTTPException(status_code=400, detail="Customer ID is not correct")

        # get info from customer service
        customer = self.customer.get_user_by_id(db, notify.customer_id)
        if customer.birth_date != notify_cancel.birth_date:
            raise HTTPException(status_code=400, detail="Birth date is not correct")

        if notify.is_read:
            raise HTTPException(status_code=400, detail="Notify has been read")

        notify.is_cancel = True
        db.commit()
        return self.get_notify_by_id(db, notify_id)

    def delete_notify(self, db: Session, notify_id: int) -> str:
        pass
