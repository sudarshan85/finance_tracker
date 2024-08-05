from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import get_db
from app.db.models import Base
from app.schemas.query import QueryParams, FilterCondition, SortOrder

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

def test_query_categories():
    # Setup: Create multiple categories
    categories = [
        {"name": "Food", "type": "expense", "monthly_budget": 500.0},
        {"name": "Rent", "type": "expense", "monthly_budget": 1000.0},
        {"name": "Salary", "type": "income", "monthly_budget": 3000.0},
    ]
    created_categories = []
    for category in categories:
        response = client.post("/api/v1/categories/", json=category)
        created_categories.append(response.json())

    # Test 1: Query all categories (no filters)
    query_params = QueryParams()
    response = client.post("/api/v1/categories/query", json=query_params.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= len(categories)

    # Test 2: Query with type filter
    query_params = QueryParams(
        filters=[
            FilterCondition(field="type", operator="eq", value="expense", data_type="string")
        ]
    )
    response = client.post("/api/v1/categories/query", json=query_params.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert all(category["type"] == "expense" for category in data)

    # Test 3: Query with monthly_budget range
    query_params = QueryParams(
        filters=[
            FilterCondition(field="monthly_budget", operator="gt", value=700, data_type="number"),
            FilterCondition(field="monthly_budget", operator="lt", value=2000, data_type="number")
        ]
    )
    response = client.post("/api/v1/categories/query", json=query_params.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert all(700 < category["monthly_budget"] < 2000 for category in data)

    # Test 4: Query with sorting
    query_params = QueryParams(
        sort=[SortOrder(field="monthly_budget", direction="desc")]
    )
    response = client.post("/api/v1/categories/query", json=query_params.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert data[0]["monthly_budget"] >= data[-1]["monthly_budget"]

    # Test 5: Query specific category
    specific_category = created_categories[0]
    query_params = QueryParams(
        filters=[
            FilterCondition(field="id", operator="eq", value=specific_category['id'], data_type="number")
        ]
    )
    response = client.post("/api/v1/categories/query", json=query_params.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == specific_category['id']

    # Clean up
    for category in created_categories:
        client.delete(f"/api/v1/categories/{category['id']}")            