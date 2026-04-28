"""
Integration Tests — Flask API
Tests run against SQLite in-memory DB — no external services needed.
Run: pytest tests/ -v

Author: Gaurav Kumar
"""

import pytest
import json
from app import create_app, db
from app.models.user import User
from app.models.item import Item


@pytest.fixture
def app():
    """Create test app with in-memory SQLite."""
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    """Register + login, return auth headers for protected routes."""
    client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "securepassword123",
        "name": "Test User"
    })
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "securepassword123"
    })
    token = response.json["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ─────────────────────────────────────────────
# Auth Tests
# ─────────────────────────────────────────────
class TestAuth:
    def test_register_success(self, client):
        res = client.post("/api/auth/register", json={
            "email": "new@example.com",
            "password": "password123",
            "name": "New User"
        })
        assert res.status_code == 201
        assert "user_id" in res.json

    def test_register_duplicate_email(self, client):
        data = {"email": "dup@example.com", "password": "password123", "name": "User"}
        client.post("/api/auth/register", json=data)
        res = client.post("/api/auth/register", json=data)
        assert res.status_code == 409

    def test_register_missing_fields(self, client):
        res = client.post("/api/auth/register", json={"email": "x@x.com"})
        assert res.status_code == 422
        assert "Missing fields" in res.json["error"]

    def test_login_success(self, client):
        client.post("/api/auth/register", json={
            "email": "login@test.com", "password": "pass12345", "name": "User"
        })
        res = client.post("/api/auth/login", json={
            "email": "login@test.com", "password": "pass12345"
        })
        assert res.status_code == 200
        assert "access_token" in res.json
        assert "refresh_token" in res.json

    def test_login_wrong_password(self, client):
        client.post("/api/auth/register", json={
            "email": "x@x.com", "password": "correctpass", "name": "User"
        })
        res = client.post("/api/auth/login", json={
            "email": "x@x.com", "password": "wrongpass"
        })
        assert res.status_code == 401


# ─────────────────────────────────────────────
# Items CRUD Tests
# ─────────────────────────────────────────────
class TestItems:
    def test_create_item(self, client, auth_headers):
        res = client.post("/api/items", headers=auth_headers, json={
            "name": "Test Item",
            "description": "A test item",
            "tags": ["test", "demo"]
        })
        assert res.status_code == 201
        assert res.json["name"] == "Test Item"
        assert res.json["tags"] == ["test", "demo"]

    def test_list_items_empty(self, client, auth_headers):
        res = client.get("/api/items", headers=auth_headers)
        assert res.status_code == 200
        assert res.json["items"] == []

    def test_list_items_with_data(self, client, auth_headers):
        for i in range(3):
            client.post("/api/items", headers=auth_headers, json={"name": f"Item {i}"})
        res = client.get("/api/items", headers=auth_headers)
        assert res.status_code == 200
        assert res.json["pagination"]["total"] == 3

    def test_get_single_item(self, client, auth_headers):
        created = client.post("/api/items", headers=auth_headers, json={"name": "Fetch Me"})
        item_id = created.json["id"]

        res = client.get(f"/api/items/{item_id}", headers=auth_headers)
        assert res.status_code == 200
        assert res.json["name"] == "Fetch Me"

    def test_update_item(self, client, auth_headers):
        created = client.post("/api/items", headers=auth_headers, json={"name": "Old Name"})
        item_id = created.json["id"]

        res = client.put(f"/api/items/{item_id}", headers=auth_headers, json={"name": "New Name"})
        assert res.status_code == 200
        assert res.json["name"] == "New Name"

    def test_delete_item(self, client, auth_headers):
        created = client.post("/api/items", headers=auth_headers, json={"name": "Delete Me"})
        item_id = created.json["id"]

        res = client.delete(f"/api/items/{item_id}", headers=auth_headers)
        assert res.status_code == 200

        # Should no longer be accessible
        res = client.get(f"/api/items/{item_id}", headers=auth_headers)
        assert res.status_code == 404

    def test_unauthorized_access(self, client):
        """Accessing protected route without token returns 401"""
        res = client.get("/api/items")
        assert res.status_code == 401

    def test_cannot_access_other_users_items(self, client):
        """User A cannot read User B's items"""
        # User A creates item
        client.post("/api/auth/register", json={"email": "a@a.com", "password": "pass12345", "name": "A"})
        login_a = client.post("/api/auth/login", json={"email": "a@a.com", "password": "pass12345"})
        headers_a = {"Authorization": f"Bearer {login_a.json['access_token']}"}
        created = client.post("/api/items", headers=headers_a, json={"name": "Private"})
        item_id = created.json["id"]

        # User B tries to access it
        client.post("/api/auth/register", json={"email": "b@b.com", "password": "pass12345", "name": "B"})
        login_b = client.post("/api/auth/login", json={"email": "b@b.com", "password": "pass12345"})
        headers_b = {"Authorization": f"Bearer {login_b.json['access_token']}"}
        res = client.get(f"/api/items/{item_id}", headers=headers_b)
        assert res.status_code == 404


# ─────────────────────────────────────────────
# Health Check Tests
# ─────────────────────────────────────────────
class TestHealth:
    def test_health_returns_200(self, client):
        res = client.get("/api/health")
        assert res.status_code == 200
        assert res.json["status"] == "healthy"

    def test_readiness_with_db(self, client):
        res = client.get("/api/health/ready")
        assert res.status_code == 200
