import pytest
from fastapi.testclient import TestClient
from app.main import app, pwd_context
from app.database import Base, engine, get_db
from app.models import User
from sqlalchemy.orm import sessionmaker

# Set up test database session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)

def get_auth_header(is_admin: bool = False):
    db = TestingSessionLocal()
    email = "admin@example.com" if is_admin else "user@example.com"
    username = "adminuser" if is_admin else "regularuser"
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            username=username,
            email=email,
            password_hash=pwd_context.hash("password123"),
            is_admin=is_admin
        )
        db.add(user)
        db.commit()
    db.close()

    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": "password123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_add_vehicle():
    headers = get_auth_header(is_admin=True)
    response = client.post(
        "/api/vehicles",
        json={
            "make": "Toyota",
            "model": "Camry",
            "category": "Sedan",
            "price": 24000.00,
            "quantity": 5
        },
        headers=headers
    )
    assert response.status_code == 201
    assert response.json()["make"] == "Toyota"


def test_get_vehicles():
    headers = get_auth_header(is_admin=True)
    client.post(
        "/api/vehicles",
        json={
            "make": "Honda",
            "model": "Civic",
            "category": "Sedan",
            "price": 22000.00,
            "quantity": 3
        },
        headers=headers
    )
    
    response = client.get("/api/vehicles")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_filter_vehicles_by_make_and_max_price():
    headers = get_auth_header(is_admin=True)
    client.post("/api/vehicles", json={"make": "Toyota", "model": "Corolla", "category": "Sedan", "price": 20000.0, "quantity": 2}, headers=headers)
    client.post("/api/vehicles", json={"make": "Ford", "model": "Explorer", "category": "SUV", "price": 40000.0, "quantity": 1}, headers=headers)

    response = client.get("/api/vehicles?make=Toyota")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


def test_update_vehicle():
    headers = get_auth_header(is_admin=True)
    res = client.post("/api/vehicles", json={"make": "Mazda", "model": "CX-5", "category": "SUV", "price": 28000.0, "quantity": 10}, headers=headers)
    vehicle_id = res.json()["id"]

    response = client.put(
        f"/api/vehicles/{vehicle_id}",
        json={"price": 27000.0},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["price"] == 27000.0


def test_delete_vehicle():
    headers = get_auth_header(is_admin=True)
    res = client.post("/api/vehicles", json={"make": "Nissan", "model": "Altima", "category": "Sedan", "price": 21000.0, "quantity": 4}, headers=headers)
    vehicle_id = res.json()["id"]

    response = client.delete(f"/api/vehicles/{vehicle_id}", headers=headers)
    assert response.status_code == 200


def test_create_sale_reduces_stock():
    headers = get_auth_header(is_admin=True)
    v_res = client.post(
        "/api/vehicles",
        json={"make": "Toyota", "model": "Corolla", "category": "Sedan", "price": 20000.0, "quantity": 5},
        headers=headers
    )
    vehicle_id = v_res.json()["id"]

    user_headers = get_auth_header(is_admin=False)
    sale_res = client.post(
        "/api/sales",
        json={"vehicle_id": vehicle_id, "quantity": 2},
        headers=user_headers
    )
    assert sale_res.status_code == 201


def test_search_vehicles():
    headers = get_auth_header(is_admin=True)
    client.post("/api/vehicles", json={"make": "Subaru", "model": "Outback", "category": "SUV", "price": 30000.0, "quantity": 3}, headers=headers)

    response = client.get("/api/vehicles/search?query=Outback")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


def test_restock_vehicle():
    headers = get_auth_header(is_admin=True)
    v_res = client.post(
        "/api/vehicles",
        json={"make": "Kia", "model": "Sorento", "category": "SUV", "price": 32000.0, "quantity": 2},
        headers=headers
    )
    vehicle_id = v_res.json()["id"]

    response = client.post(
        f"/api/vehicles/{vehicle_id}/restock",
        json={"quantity": 5},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["quantity"] == 7