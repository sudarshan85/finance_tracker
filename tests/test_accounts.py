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

def test_create_account():
    response = client.post(
        "/api/v1/accounts/",
        json={"name": "Test Account", "type": "checking", "balance": 1000.0},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Account"
    assert "id" in data

def test_read_accounts():
    response = client.post("/api/v1/accounts/query", json=QueryParams().model_dump())
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_read_account():
    # First, create an account
    create_response = client.post(
        "/api/v1/accounts/",
        json={"name": "Test Account 2", "type": "savings", "balance": 2000.0},
    )
    create_data = create_response.json()
    
    # Then, read it
    response = client.get(f"/api/v1/accounts/{create_data['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Account 2"

def test_update_account():
    # First, create an account
    create_response = client.post(
        "/api/v1/accounts/",
        json={"name": "Test Account 3", "type": "checking", "balance": 3000.0},
    )
    create_data = create_response.json()
    
    # Then, update it
    response = client.put(
        f"/api/v1/accounts/{create_data['id']}",
        json={"name": "Updated Account", "balance": 3500.0},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Account"
    assert data["balance"] == 3500.0

def test_delete_account():
    # First, create an account
    create_response = client.post(
        "/api/v1/accounts/",
        json={"name": "Test Account 4", "type": "savings", "balance": 4000.0},
    )
    create_data = create_response.json()
    
    # Then, delete it
    response = client.delete(f"/api/v1/accounts/{create_data['id']}")
    assert response.status_code == 200
    
    # Try to get the deleted account
    get_response = client.get(f"/api/v1/accounts/{create_data['id']}")
    assert get_response.status_code == 404

def test_query_accounts():
    # Setup: Create multiple accounts
    accounts = [
        {"name": "Checking 1", "type": "checking", "balance": 1000.0},
        {"name": "Savings 1", "type": "savings", "balance": 5000.0},
        {"name": "Checking 2", "type": "checking", "balance": 2000.0},
    ]
    created_accounts = []
    for account in accounts:
        response = client.post("/api/v1/accounts/", json=account)
        created_accounts.append(response.json())

    # Test 1: Query all accounts (no filters)
    query_params = QueryParams()
    response = client.post("/api/v1/accounts/query", json=query_params.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= len(accounts)

    # Test 2: Query with type filter
    query_params = QueryParams(
        filters=[
            FilterCondition(field="type", operator="eq", value="checking", data_type="string")
        ]
    )
    response = client.post("/api/v1/accounts/query", json=query_params.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert all(account["type"] == "checking" for account in data)

    # Test 3: Query with balance range
    query_params = QueryParams(
        filters=[
            FilterCondition(field="balance", operator="gt", value=1500, data_type="number"),
            FilterCondition(field="balance", operator="lt", value=5500, data_type="number")
        ]
    )
    response = client.post("/api/v1/accounts/query", json=query_params.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert all(1500 < account["balance"] < 5500 for account in data)

    # Test 4: Query with sorting
    query_params = QueryParams(
        sort=[SortOrder(field="balance", direction="desc")]
    )
    response = client.post("/api/v1/accounts/query", json=query_params.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert data[0]["balance"] >= data[-1]["balance"]

    # Test 5: Query specific account
    specific_account = created_accounts[0]
    query_params = QueryParams(
        filters=[
            FilterCondition(field="id", operator="eq", value=specific_account['id'], data_type="number")
        ]
    )
    response = client.post("/api/v1/accounts/query", json=query_params.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == specific_account['id']

    # Clean up
    for account in created_accounts:
        client.delete(f"/api/v1/accounts/{account['id']}")

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