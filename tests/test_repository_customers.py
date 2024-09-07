import pytest
from app.models.pydantic_models import CustomerCreate


def test_create_customer(customer_repository):
    customer_data = CustomerCreate(
        name={
            "prefix": "Mr",
            "surname": "Doe",
            "middle_name": "John",
            "family_name": "Smith",
            "suffix": "Jr"
        },
        email="john.doe@example.com",
        phone_number="1234567890"
    )
    customer = customer_repository.create(customer_data)
    assert customer.email == customer_data.email
    assert customer.id is not None


def test_get_customer(customer_repository):
    customer_data = CustomerCreate(
        name={
            "prefix": "Ms",
            "surname": "Doe",
            "middle_name": "Jane",
            "family_name": "Smith",
            "suffix": "Sr"
        },
        email="jane.doe@example.com",
        phone_number="9876543210"
    )
    created_customer = customer_repository.create(customer_data)

    retrieved_customer = customer_repository.get_by_id(created_customer.id)
    assert retrieved_customer is not None
    assert retrieved_customer.email == customer_data.email


def test_update_customer(customer_repository):
    customer_data = CustomerCreate(
        name={
            "prefix": "Mr",
            "surname": "Doe",
            "middle_name": "John",
            "family_name": "Smith",
            "suffix": "Jr"
        },
        email="john.doe@example.com",
        phone_number="1234567890"
    )
    created_customer = customer_repository.create(customer_data)

    update_data = CustomerCreate(
        name={
            "prefix": "Mr",
            "surname": "Doe",
            "middle_name": "Johnny",
            "family_name": "Smith",
            "suffix": "Sr"
        },
        email="johnny.doe@example.com",
        phone_number="9876543210"
    )
    updated_customer = customer_repository.update(created_customer.id, update_data)
    assert updated_customer is not None
    assert updated_customer.email == update_data.email
    assert updated_customer.name.middle_name == update_data.name.middle_name


def test_delete_customer(customer_repository):
    customer_data = CustomerCreate(
        name={
            "prefix": "Mrs",
            "surname": "Doe",
            "middle_name": "Janet",
            "family_name": "Smith",
            "suffix": ""
        },
        email="janet.doe@example.com",
        phone_number="5555555555"
    )
    created_customer = customer_repository.create(customer_data)

    assert customer_repository.delete(created_customer.id) is True
    assert customer_repository.get_by_id(created_customer.id) is None


def test_get_customer_by_email(customer_repository):
    customer_data = CustomerCreate(
        name={
            "prefix": "Dr",
            "surname": "Doe",
            "middle_name": "James",
            "family_name": "Smith",
            "suffix": "PhD"
        },
        email="james.doe@example.com",
        phone_number="1122334455"
    )
    customer_repository.create(customer_data)

    retrieved_customer = customer_repository.get_by_email(customer_data.email)
    assert retrieved_customer is not None
    assert retrieved_customer.email == customer_data.email
    assert retrieved_customer.name.middle_name == customer_data.name.middle_name