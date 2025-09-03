import pytest
from fastapi.testclient import TestClient
from backend.main import app
import os

# Set test environment
os.environ['DATABASE_URL'] = 'sqlite:///./test.db'

client = TestClient(app)

class TestFounderPortal:
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert "status" in response.json()
        assert response.json()["status"] == "healthy"

    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
        assert "AstraNetix" in response.json()["message"]

    def test_auth_endpoints_exist(self):
        """Test that auth endpoints are accessible"""
        # Test login endpoint exists (should return 422 for invalid data, not 404)
        response = client.post("/api/auth/login", json={})
        assert response.status_code != 404

    def test_founder_endpoints_exist(self):
        """Test that founder endpoints exist"""
        # Should return 401 for unauthorized access, not 404
        response = client.get("/api/founder/dashboard")
        assert response.status_code == 401  # Unauthorized, not Not Found

class TestDatabaseModels:
    def test_models_import(self):
        """Test that database models can be imported"""
        from backend.shared.models.models import Founder, ISP, Branch, User
        
        # Models should be importable
        assert Founder is not None
        assert ISP is not None
        assert Branch is not None
        assert User is not None

class TestUtilities:
    def test_security_utils(self):
        """Test security utility functions"""
        from backend.shared.utils.security import hash_password, verify_password, generate_domain_safe_string
        
        # Test password hashing
        password = "test123"
        hashed = hash_password(password)
        assert hashed != password
        assert verify_password(password, hashed)
        assert not verify_password("wrong", hashed)
        
        # Test domain generation
        domain = generate_domain_safe_string("Test Company Name!")
        assert domain == "test-company-name"
        assert "-" not in domain[0]  # Should not start with hyphen
        assert "-" not in domain[-1]  # Should not end with hyphen

    def test_config_loading(self):
        """Test configuration loading"""
        from backend.shared.config import settings
        
        assert settings is not None
        assert hasattr(settings, 'app_name')
        assert hasattr(settings, 'database_url')