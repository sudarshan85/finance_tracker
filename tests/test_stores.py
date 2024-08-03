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

def test_create_store():
    response = client.post(
        "/api/v1/stores/",
        json={"name": "Test Store", "user_defined": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Store"
    assert "id" in data

def test_read_stores():
    response = client.get("/api/v1/stores/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_read_store():
    # First, create a store
    create_response = client.post(
        "/api/v1/stores/",
        json={"name": "Test Store 2", "user_defined": True},
    )
    create_data = create_response.json()
    
    # Then, read it
    response = client.get(f"/api/v1/stores/{create_data['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Store 2"

def test_update_store():
    # First, create a store
    create_response = client.post(
        "/api/v1/stores/",
        json={"name": "Test Store 3", "user_defined": True},
    )
    create_data = create_response.json()
    
    # Then, update it
    response = client.put(
        f"/api/v1/stores/{create_data['id']}",
        json={"name": "Updated Store"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Store"

def test_delete_store():
    # First, create a store
    create_response = client.post(
        "/api/v1/stores/",
        json={"name": "Test Store 4", "user_defined": True},
    )
    create_data = create_response.json()
    
    # Then, delete it
    response = client.delete(f"/api/v1/stores/{create_data['id']}")
    assert response.status_code == 200
    
    # Try to get the deleted store
    get_response = client.get(f"/api/v1/stores/{create_data['id']}")
    assert get_response.status_code == 404
