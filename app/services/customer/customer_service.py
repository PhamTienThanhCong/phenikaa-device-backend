from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.services.customer.customer_schema import CustomerBase, CustomerUpdate
from .customer_model import Customer

class CustomerService:
  def __init__(self):
    pass

  def get_health(self):
    return "OK"
  
  def get_user_by_id(self, db: Session, id: int):
    print(":id", id)
    return db.query(Customer).filter(Customer.id == id).first()
  
  # create new user
  def create_user(self, db: Session, user: CustomerBase):
    new_user = Customer(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
  
  # get all users
  def get_all_users(self, db: Session, limit: int, offset: int):
    return db.query(Customer).offset(offset).limit(limit).all()
  
  # update user
  def update_user(self, db: Session, user: CustomerUpdate, id: int):
    db.query(Customer).filter(Customer.id == id).update(user.dict())
    db.commit()
    return db.query(Customer).filter(Customer.id == id).first()
  
  # delete user
  def delete_user(self, db: Session, id: int):
    db.query(Customer).filter(Customer.id == id).delete()
    db.commit()
    return JSONResponse(content={"message": "User deleted successfully"}, status_code=200)