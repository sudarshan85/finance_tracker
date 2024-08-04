from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import get_db
from app.db.models import Base
from app.schemas.query import QueryParams

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

def test_create_category():
    response = client.post(
        "/api/v1/categories/",
        json={"name": "Test Category", "type": "expense", "monthly_budget": 100.0},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Category"
    assert "id" in data

def test_read_categories():
    response = client.post("/api/v1/categories/query", json=QueryParams().model_dump())
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_read_category():
    # First, create a category
    create_response = client.post(
        "/api/v1/categories/",
        json={"name": "Test Category 2", "type": "income", "monthly_budget": 500.0},
    )
    create_data = create_response.json()
    
    # Then, read it
    response = client.get(f"/api/v1/categories/{create_data['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Category 2"

def test_update_category():
    # First, create a category
    create_response = client.post(
        "/api/v1/categories/",
        json={"name": "Test Category 3", "type": "expense", "monthly_budget": 300.0},
    )
    create_data = create_response.json()
    
    # Then, update it
    response = client.put(
        f"/api/v1/categories/{create_data['id']}",
        json={"name": "Updated Category", "monthly_budget": 400.0},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Category"
    assert data["monthly_budget"] == 400.0

def test_delete_category():
    # First, create a category
    create_response = client.post(
        "/api/v1/categories/",
        json={"name": "Test Category 4", "type": "income", "monthly_budget": 1000.0},
    )
    create_data = create_response.json()
    
    # Then, delete it
    response = client.delete(f"/api/v1/categories/{create_data['id']}")
    assert response.status_code == 200
    
    # Try to get the deleted category
    get_response = client.get(f"/api/v1/categories/{create_data['id']}")
    assert get_response.status_code == 404