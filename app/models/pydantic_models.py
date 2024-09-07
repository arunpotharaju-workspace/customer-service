from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Generic, TypeVar

T = TypeVar('T')

class CustomerName(BaseModel):
    prefix: Optional[str] = Field(None, max_length=10)
    surname: str = Field(..., min_length=1, max_length=50)
    middle_name: Optional[str] = Field(None, max_length=50)
    family_name: str = Field(..., min_length=1, max_length=50)
    suffix: Optional[str] = Field(None, max_length=10)

class CustomerCreate(BaseModel):
    name: CustomerName
    email: EmailStr
    phone_number: str = Field(min_length=10)

class Customer(CustomerCreate):
    id: str

    class Config:
        from_attributes = True

class VersionedResponse(BaseModel, Generic[T]):
    api_version: str = "1.0"
    data: T