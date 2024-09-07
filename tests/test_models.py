import pytest
from pydantic import ValidationError
from app.models.pydantic_models import CustomerCreate, Customer

def test_valid_customer_create():
    customer_data = {
        "name": {
            "prefix": "Mr",
            "surname": "Doe",
            "middle_name": "John",
            "family_name": "Smith",
            "suffix": "Jr"
        },
        "email": "john.doe@example.com",
        "phone_number": "1234567890"
    }
    customer = CustomerCreate(**customer_data)
    assert customer.email == customer_data["email"]
    assert customer.name.surname == customer_data["name"]["surname"]

def test_invalid_email():
    customer_data = {
        "name": {
            "prefix": "Mr",
            "surname": "Doe",
            "middle_name": "John",
            "family_name": "Smith",
            "suffix": "Jr"
        },
        "email": "invalid-email",
        "phone_number": "1234567890"
    }
    with pytest.raises(ValidationError):
        CustomerCreate(**customer_data)

def test_invalid_phone_number():
    customer_data = {
        "name": {
            "prefix": "Mr",
            "surname": "Doe",
            "middle_name": "John",
            "family_name": "Smith",
            "suffix": "Jr"
        },
        "email": "john.doe@example.com",
        "phone_number": "123"  # Too short
    }
    with pytest.raises(ValidationError):
        CustomerCreate(**customer_data)

def test_customer_model():
    customer_data = {
        "id": "12345",
        "name": {
            "prefix": "Mr",
            "surname": "Doe",
            "middle_name": "John",
            "family_name": "Smith",
            "suffix": "Jr"
        },
        "email": "john.doe@example.com",
        "phone_number": "1234567890"
    }
    customer = Customer(**customer_data)
    assert customer.id == customer_data["id"]
    assert customer.email == customer_data["email"]
    assert customer.name.surname == customer_data["name"]["surname"]