from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import get_db
from app.db.models import Base
from app.schemas.query import QueryParams, FilterCondition, SortOrder
from datetime import date, timedelta

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

def setup_test_data():
    # Create test accounts
    accounts = [
        {"name": "Checking", "type": "checking", "balance": 1000.0},
        {"name": "Savings", "type": "savings", "balance": 5000.0},
    ]
    account_ids = []
    for account in accounts:
        response = client.post("/api/v1/accounts/", json=account)
        account_ids.append(response.json()["id"])

    # Create test categories
    categories = [
        {"name": "Food", "type": "expense", "monthly_budget": 500.0},
        {"name": "Salary", "type": "income", "monthly_budget": 3000.0},
    ]
    category_ids = []
    for category in categories:
        response = client.post("/api/v1/categories/", json=category)
        category_ids.append(response.json()["id"])

    # Create test transactions
    transactions = [
        {
            "date": str(date.today() - timedelta(days=5)),
            "amount": 50.0,
            "description": "Grocery shopping",
            "account_id": account_ids[0],
            "category_id": category_ids[0],
        },
        {
            "date": str(date.today() - timedelta(days=3)),
            "amount": 3000.0,
            "description": "Monthly salary",
            "account_id": account_ids[1],
            "category_id": category_ids[1],
        },
        {
            "date": str(date.today() - timedelta(days=1)),
            "amount": 100.0,
            "description": "Restaurant dinner",
            "account_id": account_ids[0],
            "category_id": category_ids[0],
        },
    ]
    for transaction in transactions:
        client.post("/api/v1/transactions/", json=transaction)

def test_complex_transaction_query():
    setup_test_data()

    # Test query with multiple filters and sorting
    query_params = QueryParams(
        filters=[
            FilterCondition(field="amount", operator="gt", value=75, data_type="number"),
            FilterCondition(field="date", operator="gt", value=str(date.today() - timedelta(days=4)), data_type="date"),
        ],
        sort=[SortOrder(field="amount", direction="desc")]
    )
    response = client.post("/api/v1/transactions/query", json=query_params.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["items"][0]["amount"] == 3000.0
    assert data["items"][1]["amount"] == 100.0

def test_category_query_with_budget_filter():
    # Test query for categories with monthly budget greater than 1000
    query_params = QueryParams(
        filters=[
            FilterCondition(field="monthly_budget", operator="gt", value=1000, data_type="number"),
        ]
    )
    response = client.post("/api/v1/categories/query", json=query_params.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "Salary"

def test_account_query_with_type_filter():
    # Test query for checking accounts
    query_params = QueryParams(
        filters=[
            FilterCondition(field="type", operator="eq", value="checking", data_type="string"),
        ]
    )
    response = client.post("/api/v1/accounts/query", json=query_params.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) > 0  # Check if there's at least one checking account
    assert all(account["type"] == "checking" for account in data["items"])  # Ensure all returned accounts are of type "checking"
    
def test_pagination():
    # Test pagination for transactions
    query_params = QueryParams(skip=1, limit=1)
    response = client.post("/api/v1/transactions/query", json=query_params.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["total"] == 3
    assert data["page"] == 2
    assert data["size"] == 1

# Add more complex query tests as needed