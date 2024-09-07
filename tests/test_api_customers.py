import pytest
from app.models.pydantic_models import CustomerCreate

def test_create_customer(client):
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
    response = client.post("/api/v1/customers", json=customer_data)
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["email"] == customer_data["email"]
    assert "id" in data

def test_get_customer(client):
    # First, create a customer
    customer_data = {
        "name": {
            "prefix": "Ms",
            "surname": "Doe",
            "middle_name": "Jane",
            "family_name": "Smith",
            "suffix": "Sr"
        },
        "email": "jane.doe@example.com",
        "phone_number": "9876543210"
    }
    create_response = client.post("/api/v1/customers", json=customer_data)
    customer_id = create_response.json()["data"]["id"]

    # Now, get the customer
    response = client.get(f"/api/v1/customers/{customer_id}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["email"] == customer_data["email"]

def test_update_customer(client):
    # First, create a customer
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
    create_response = client.post("/api/v1/customers", json=customer_data)
    customer_id = create_response.json()["data"]["id"]

    # Now, update the customer
    update_data = {
        "name": {
            "prefix": "Mr",
            "surname": "Doe",
            "middle_name": "Johnny",
            "family_name": "Smith",
            "suffix": "Sr"
        },
        "email": "johnny.doe@example.com",
        "phone_number": "9876543210"
    }
    response = client.put(f"/api/v1/customers/{customer_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["email"] == update_data["email"]
    assert data["name"]["middle_name"] == update_data["name"]["middle_name"]

def test_delete_customer(client):
    # First, create a customer
    customer_data = {
        "name": {
            "prefix": "Mrs",
            "surname": "Doe",
            "middle_name": "Janet",
            "family_name": "Smith",
            "suffix": ""
        },
        "email": "janet.doe@example.com",
        "phone_number": "5555555555"
    }
    create_response = client.post("/api/v1/customers", json=customer_data)
    customer_id = create_response.json()["data"]["id"]

    # Now, delete the customer
    response = client.delete(f"/api/v1/customers/{customer_id}")
    assert response.status_code == 200

    # Try to get the deleted customer
    get_response = client.get(f"/api/v1/customers/{customer_id}")
    assert get_response.status_code == 404

def test_get_customer_by_email(client):
    # First, create a customer
    customer_data = {
        "name": {
            "prefix": "Dr",
            "surname": "Doe",
            "middle_name": "James",
            "family_name": "Smith",
            "suffix": "PhD"
        },
        "email": "james.doe@example.com",
        "phone_number": "1122334455"
    }
    client.post("/api/v1/customers", json=customer_data)

    # Now, get the customer by email
    response = client.get(f"/api/v1/customers/email/{customer_data['email']}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["email"] == customer_data["email"]
    assert data["name"]["middle_name"] == customer_data["name"]["middle_name"]