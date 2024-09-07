from sqlalchemy import Column, String, JSON
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class CustomerModel(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(JSON, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=False)