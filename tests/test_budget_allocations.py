from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import get_db
from app.db.models import Base

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

def test_create_budget_allocation():
    # First, create a category
    category_response = client.post(
        "/api/v1/categories/",
        json={"name": "Test Category", "type": "expense", "monthly_budget": 100.0},
    )
    category_data = category_response.json()
    
    # Now create a budget allocation
    response = client.post(
        "/api/v1/budget_allocations/",
        json={
            "year": 2023,
            "month": 5,
            "amount": 150.0,
            "category_id": category_data["id"]
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["year"] == 2023
    assert data["month"] == 5
    assert data["amount"] == 150.0
    assert "id" in data

def test_read_budget_allocations():
    response = client.get("/api/v1/budget_allocations/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_read_budget_allocation():
    # First, create a budget allocation
    category_response = client.post(
        "/api/v1/categories/",
        json={"name": "Test Category 2", "type": "income", "monthly_budget": 500.0},
    )
    category_data = category_response.json()
    
    create_response = client.post(
        "/api/v1/budget_allocations/",
        json={
            "year": 2023,
            "month": 6,
            "amount": 200.0,
            "category_id": category_data["id"]
        },
    )
    create_data = create_response.json()
    
    # Then, read it
    response = client.get(f"/api/v1/budget_allocations/{create_data['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["year"] == 2023
    assert data["month"] == 6
    assert data["amount"] == 200.0

def test_update_budget_allocation():
    # First, create a budget allocation
    category_response = client.post(
        "/api/v1/categories/",
        json={"name": "Test Category 3", "type": "expense", "monthly_budget": 300.0},
    )
    category_data = category_response.json()
    
    create_response = client.post(
        "/api/v1/budget_allocations/",
        json={
            "year": 2023,
            "month": 7,
            "amount": 250.0,
            "category_id": category_data["id"]
        },
    )
    create_data = create_response.json()
    
    # Then, update it
    response = client.put(
        f"/api/v1/budget_allocations/{create_data['id']}",
        json={"amount": 300.0},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 300.0

def test_delete_budget_allocation():
    # First, create a budget allocation
    category_response = client.post(
        "/api/v1/categories/",
        json={"name": "Test Category 4", "type": "income", "monthly_budget": 1000.0},
    )
    category_data = category_response.json()
    
    create_response = client.post(
        "/api/v1/budget_allocations/",
        json={
            "year": 2023,
            "month": 8,
            "amount": 1200.0,
            "category_id": category_data["id"]
        },
    )
    create_data = create_response.json()
    
    # Then, delete it
    response = client.delete(f"/api/v1/budget_allocations/{create_data['id']}")
    assert response.status_code == 200
    
    # Try to get the deleted budget allocation
    get_response = client.get(f"/api/v1/budget_allocations/{create_data['id']}")
    assert get_response.status_code == 404
