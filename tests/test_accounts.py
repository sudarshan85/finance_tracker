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