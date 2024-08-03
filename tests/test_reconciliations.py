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

def test_create_reconciliation():
    # First, create an account
    account_response = client.post(
        "/api/v1/accounts/",
        json={"name": "Test Account", "type": "checking", "balance": 1000.0},
    )
    account_data = account_response.json()
    
    # Create a reconciliation
    reconciliation_date = str(date.today())
    response = client.post(
        "/api/v1/reconciliations/",
        json={"date": reconciliation_date, "account_id": account_data["id"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["date"] == reconciliation_date
    assert data["account_id"] == account_data["id"]

def test_get_last_reconciliation():
    # First, create an account
    account_response = client.post(
        "/api/v1/accounts/",
        json={"name": "Test Account 2", "type": "savings", "balance": 2000.0},
    )
    account_data = account_response.json()
    
    # Create two reconciliations
    first_date = str(date(2023, 1, 1))
    second_date = str(date(2023, 2, 1))
    
    client.post(
        "/api/v1/reconciliations/",
        json={"date": first_date, "account_id": account_data["id"]},
    )
    client.post(
        "/api/v1/reconciliations/",
        json={"date": second_date, "account_id": account_data["id"]},
    )
    
    # Get last reconciliation
    response = client.get(f"/api/v1/reconciliations/{account_data['id']}/last")
    assert response.status_code == 200
    data = response.json()
    assert data["date"] == second_date
    assert data["account_id"] == account_data["id"]

def test_account_last_reconciled_update():
    # Create an account
    account_response = client.post(
        "/api/v1/accounts/",
        json={"name": "Test Account 3", "type": "checking", "balance": 3000.0},
    )
    account_data = account_response.json()
    
    # Create a reconciliation
    reconciliation_date = str(date.today())
    client.post(
        "/api/v1/reconciliations/",
        json={"date": reconciliation_date, "account_id": account_data["id"]},
    )
    
    # Check if the account's last_reconciled date was updated
    account_response = client.get(f"/api/v1/accounts/{account_data['id']}")
    updated_account_data = account_response.json()
    assert updated_account_data["last_reconciled"] == reconciliation_date