from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import get_db
from app.db.models import Base
from datetime import date

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_transaction():
    # First, create an account and a category
    account_response = client.post(
        "/api/v1/accounts/",
        json={"name": "Test Account", "type": "checking", "balance": 1000.0},
    )
    account_data = account_response.json()
    
    category_response = client.post(
        "/api/v1/categories/",
        json={"name": "Test Category", "type": "expense", "monthly_budget": 100.0},
    )
    category_data = category_response.json()
    
    response = client.post(
        "/api/v1/transactions/",
        json={
            "date": str(date.today()),
            "amount": 50.0,
            "description": "Test Transaction",
            "account_id": account_data["id"],
            "category_id": category_data["id"],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Test Transaction"
    assert data["status"] == "PENDING"
    assert "id" in data

def test_read_transactions():
    response = client.get("/api/v1/transactions/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_update_transaction():
    # First, create a transaction
    account_response = client.post(
        "/api/v1/accounts/",
        json={"name": "Test Account 2", "type": "savings", "balance": 2000.0},
    )
    account_data = account_response.json()
    
    category_response = client.post(
        "/api/v1/categories/",
        json={"name": "Test Category 2", "type": "income", "monthly_budget": 500.0},
    )
    category_data = category_response.json()
    
    create_response = client.post(
        "/api/v1/transactions/",
        json={
            "date": str(date.today()),
            "amount": 100.0,
            "description": "Test Transaction 2",
            "account_id": account_data["id"],
            "category_id": category_data["id"],
        },
    )
    create_data = create_response.json()
    
    # Then, update it
    response = client.put(
        f"/api/v1/transactions/{create_data['id']}",
        json={"description": "Updated Transaction", "amount": 150.0},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Updated Transaction"
    assert data["amount"] == 150.0

def test_complete_transaction():
    # First, create a transaction
    account_response = client.post(
        "/api/v1/accounts/",
        json={"name": "Test Account 3", "type": "checking", "balance": 3000.0},
    )
    account_data = account_response.json()
    
    category_response = client.post(
        "/api/v1/categories/",
        json={"name": "Test Category 3", "type": "expense", "monthly_budget": 300.0},
    )
    category_data = category_response.json()
    
    create_response = client.post(
        "/api/v1/transactions/",
        json={
            "date": str(date.today()),
            "amount": 200.0,
            "description": "Test Transaction 3",
            "account_id": account_data["id"],
            "category_id": category_data["id"],
        },
    )
    create_data = create_response.json()
    
    # Then, complete it
    response = client.put(f"/api/v1/transactions/{create_data['id']}/complete")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "COMPLETED"