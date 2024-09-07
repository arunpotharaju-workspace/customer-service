from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.models.pydantic_models import Customer, CustomerCreate, VersionedResponse
from app.repositories.customer_repository import CustomerRepository
from app.database import get_db
from app.core.logging import logger
from app.utils.telemetry import increment_customer_created, increment_customer_updated, increment_customer_deleted
from opentelemetry import trace

router = APIRouter()
tracer = trace.get_tracer(__name__)

def get_repository(db: Session = Depends(get_db)):
    return CustomerRepository(db)

@router.post("/customers", response_model=VersionedResponse[Customer], status_code=201)
async def create_customer(
    customer: CustomerCreate,
    repo: CustomerRepository = Depends(get_repository)
):
    with tracer.start_as_current_span("create_customer"):
        logger.info("Creating new customer", privacy_level="MEDIUM")
        try:
            new_customer = repo.create(customer)
            increment_customer_created()
            logger.info("Customer created successfully", privacy_level="LOW", customer_id=new_customer.id)
            return VersionedResponse(data=new_customer)
        except Exception as e:
            logger.error("Error creating customer", privacy_level="HIGH", error=str(e))
            raise HTTPException(status_code=500, detail="Error creating customer")

@router.get("/customers", response_model=VersionedResponse[List[Customer]])
async def get_all_customers(repo: CustomerRepository = Depends(get_repository)):
    with tracer.start_as_current_span("get_all_customers"):
        logger.info("Fetching all customers", privacy_level="LOW")
        customers = repo.get_all()
        return VersionedResponse(data=customers)

@router.get("/customers/{customer_id}", response_model=VersionedResponse[Customer])
async def get_customer(
    customer_id: str,
    repo: CustomerRepository = Depends(get_repository)
):
    with tracer.start_as_current_span("get_customer"):
        logger.info("Fetching customer", privacy_level="MEDIUM", customer_id=customer_id)
        customer = repo.get_by_id(customer_id)
        if not customer:
            logger.warning("Customer not found", privacy_level="MEDIUM", customer_id=customer_id)
            raise HTTPException(status_code=404, detail="Customer not found")
        return VersionedResponse(data=customer)

@router.get("/customers/email/{email}", response_model=VersionedResponse[Customer])
async def get_customer_by_email(
    email: str,
    repo: CustomerRepository = Depends(get_repository)
):
    with tracer.start_as_current_span("get_customer_by_email"):
        logger.info("Fetching customer by email", privacy_level="MEDIUM", email=email)
        customer = repo.get_by_email(email)
        if not customer:
            logger.warning("Customer not found", privacy_level="MEDIUM", email=email)
            raise HTTPException(status_code=404, detail="Customer not found")
        return VersionedResponse(data=customer)

@router.put("/customers/{customer_id}", response_model=VersionedResponse[Customer])
async def update_customer(
    customer_id: str,
    customer_update: CustomerCreate,
    repo: CustomerRepository = Depends(get_repository)
):
    with tracer.start_as_current_span("update_customer"):
        logger.info("Updating customer", privacy_level="MEDIUM", customer_id=customer_id)
        updated_customer = repo.update(customer_id, customer_update)
        if not updated_customer:
            logger.warning("Customer not found for update", privacy_level="MEDIUM", customer_id=customer_id)
            raise HTTPException(status_code=404, detail="Customer not found")
        increment_customer_updated()
        logger.info("Customer updated successfully", privacy_level="LOW", customer_id=customer_id)
        return VersionedResponse(data=updated_customer)

@router.delete("/customers/{customer_id}", response_model=VersionedResponse[dict])
async def delete_customer(
    customer_id: str,
    repo: CustomerRepository = Depends(get_repository)
):
    with tracer.start_as_current_span("delete_customer"):
        logger.info("Deleting customer", privacy_level="MEDIUM", customer_id=customer_id)
        if not repo.delete(customer_id):
            logger.warning("Customer not found for deletion", privacy_level="MEDIUM", customer_id=customer_id)
            raise HTTPException(status_code=404, detail="Customer not found")
        increment_customer_deleted()
        logger.info("Customer deleted successfully", privacy_level="LOW", customer_id=customer_id)
        return VersionedResponse(data={"message": "Customer deleted successfully"})