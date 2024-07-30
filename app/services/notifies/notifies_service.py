import datetime
import json
from typing import Any, List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.services.customer.customer_service import CustomerService
from app.services.notifies.notifies_model import Notify
from app.services.notifies.notifies_schema import (
    NotifySchemaBase,
    NotifySchemaCreate,
    NotifySchemaUpdate,
)
from app.services.users.user_service import UserService


class NotifyService:
    def __init__(self):
        self.customer = CustomerService()
        self.user = UserService()

    def get_notifies(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[NotifySchemaBase]:
        notifies = (
            db.query(Notify).order_by(Notify.created_at).offset(skip).limit(limit).all()
        )
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
        return notify

    def create_notify(
        self, db: Session, notify: NotifySchemaCreate
    ) -> NotifySchemaBase:
        data = notify.dict()

        created_at = datetime.datetime.now()
        data["created_at"] = created_at
        self.customer.validate_customer(db, data["customer_id"])

        new_notify = Notify(**data)
        db.add(new_notify)
        db.commit()
        db.refresh(new_notify)
        return "ok"

    def make_read_notify(
        self,
        db: Session,
        notify_id: int,
        explain_data: NotifySchemaUpdate,
        user_id: int,
    ) -> str:
        notify = db.query(Notify).filter(Notify.id == notify_id).first()
        explain_data = explain_data.dict()
        notify.explain = explain_data["explain"]
        if notify is None:
            raise HTTPException(status_code=404, detail="Notify not found")
        notify.is_read = True
        notify.user_id = user_id
        notify.confirmed_at = datetime.datetime.now()
        db.commit()
        return self.get_notify_by_id(db, notify_id)

    def delete_notify(self, db: Session, notify_id: int) -> str:
        pass
