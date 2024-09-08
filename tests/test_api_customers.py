import pytest
from app.models.pydantic_models import CustomerCreate

def test_create_customer(client, auth_headers):
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
    response = client.post("/api/v1/customers", json=customer_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["email"] == customer_data["email"]
    assert "id" in data

def test_get_customer(client, auth_headers):
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
    create_response = client.post("/api/v1/customers", json=customer_data, headers=auth_headers)
    customer_id = create_response.json()["data"]["id"]

    # Now, get the customer
    response = client.get(f"/api/v1/customers/{customer_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["email"] == customer_data["email"]

def test_update_customer(client, auth_headers):
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
    create_response = client.post("/api/v1/customers", json=customer_data, headers=auth_headers)
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
    response = client.put(f"/api/v1/customers/{customer_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["email"] == update_data["email"]
    assert data["name"]["middle_name"] == update_data["name"]["middle_name"]

def test_delete_customer(client, auth_headers):
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
    create_response = client.post("/api/v1/customers", json=customer_data, headers=auth_headers)
    customer_id = create_response.json()["data"]["id"]

    # Now, delete the customer
    response = client.delete(f"/api/v1/customers/{customer_id}", headers=auth_headers)
    assert response.status_code == 200

    # Try to get the deleted customer
    get_response = client.get(f"/api/v1/customers/{customer_id}", headers=auth_headers)
    assert get_response.status_code == 404

def test_get_customer_by_email(client, auth_headers):
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
    client.post("/api/v1/customers", json=customer_data, headers=auth_headers)

    # Now, get the customer by email
    response = client.get(f"/api/v1/customers/email/{customer_data['email']}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["email"] == customer_data["email"]
    assert data["name"]["middle_name"] == customer_data["name"]["middle_name"]

def test_create_bulk_customers(client, auth_headers):
    # Create 100 customers
    created_customers = []
    for i in range(10):
        customer_data = {
            "name": {
                "prefix": "Mr",
                "surname": f"Doe{i}",
                "middle_name": f"John{i}",
                "family_name": "Smith",
                "suffix": "Jr"
            },
            "email": f"john.doe{i}@example.com",
            "phone_number": f"123456789{i % 10}"
        }
        response = client.post("/api/v1/customers", json=customer_data, headers=auth_headers)
        assert response.status_code == 201
        created_customers.append(response.json()["data"])

    # Verify that all 100 customers were created
    assert len(created_customers) == 10

    # Get all customers
    response = client.get("/api/v1/customers", headers=auth_headers)
    assert response.status_code == 200
    all_customers = response.json()["data"]

    # Verify that at least 100 customers exist (there might be more from other tests)
    assert len(all_customers) >= 10

    # Verify that all created customers exist in the returned list
    created_emails = set(customer["email"] for customer in created_customers)
    returned_emails = set(customer["email"] for customer in all_customers)
    assert created_emails.issubset(returned_emails)

    # Verify details of a few random customers
    for i in [0, 4, 9]:  # Check first, middle, and last created customer
        customer = created_customers[i]
        response = client.get(f"/api/v1/customers/{customer['id']}", headers=auth_headers)
        assert response.status_code == 200
        retrieved_customer = response.json()["data"]
        assert retrieved_customer["email"] == customer["email"]
        assert retrieved_customer["name"]["surname"] == f"Doe{i}"