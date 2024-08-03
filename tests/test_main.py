import pytest, os
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Welcome to the {settings.app_name} API"
    assert "environment" in data
    assert "debug_mode" in data

def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "environment" in data

@pytest.mark.parametrize("env", ["dev", "prod"])
def test_environment_specific_config(env, monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", env)
    monkeypatch.setenv("DEBUG", str(env == "dev"))
    
    # Print environment variables for debugging
    print(f"Set ENVIRONMENT to: {env}")
    print(f"Actual ENVIRONMENT: {os.getenv('ENVIRONMENT')}")
    
    # Reload settings
    from importlib import reload
    import app.core.config
    from app.core.config import reload_settings
    reload(app.core.config)
    new_settings = reload_settings()
    print(f"Settings environment: {new_settings.environment}")
    
    assert new_settings.environment == env, f"Expected {env}, got {new_settings.environment}"
    assert new_settings.debug == (env == "dev")