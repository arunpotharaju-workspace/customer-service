from sqlalchemy.orm import Session
from app.models.database import CustomerModel
from app.models.pydantic_models import Customer, CustomerCreate
from typing import List, Optional

class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, customer: CustomerCreate) -> Customer:
        db_customer = CustomerModel(**customer.dict())
        self.db.add(db_customer)
        self.db.commit()
        self.db.refresh(db_customer)
        return Customer.from_orm(db_customer)

    def get_all(self) -> List[Customer]:
        customers = self.db.query(CustomerModel).all()
        return [Customer.from_orm(c) for c in customers]

    def get_by_id(self, customer_id: str) -> Optional[Customer]:
        customer = self.db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
        return Customer.from_orm(customer) if customer else None

    def get_by_email(self, email: str) -> Optional[Customer]:
        customer = self.db.query(CustomerModel).filter(CustomerModel.email == email).first()
        return Customer.from_orm(customer) if customer else None

    def update(self, customer_id: str, customer_update: CustomerCreate) -> Optional[Customer]:
        db_customer = self.db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
        if not db_customer:
            return None
        for key, value in customer_update.dict().items():
            setattr(db_customer, key, value)
        self.db.commit()
        self.db.refresh(db_customer)
        return Customer.from_orm(db_customer)

    def delete(self, customer_id: str) -> bool:
        db_customer = self.db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
        if db_customer:
            self.db.delete(db_customer)
            self.db.commit()
            return True
        return False