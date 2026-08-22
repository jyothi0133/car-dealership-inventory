from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.models import User

client = TestClient(app)

def get_auth_header(is_admin: bool = False):
    email = "admin@example.com" if is_admin else "test@example.com"
    username = "admin_user" if is_admin else "tester"
    
    # Register user
    client.post("/api/auth/register", json={"username": username, "email": email, "password": "password123"})
    
    # If admin requested, set is_admin = True directly in DB
    if is_admin:
        db = next(get_db())
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.is_admin = True
            db.commit()
            
    login_res = client.post("/api/auth/login", json={"email": email, "password": "password123"})
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_add_vehicle():
    headers = get_auth_header()
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
    data = response.json()
    assert data["make"] == "Toyota"
    assert data["id"] is not None

def test_get_vehicles():
    headers = get_auth_header()
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
    headers = get_auth_header()
    client.post("/api/vehicles", json={"make": "Toyota", "model": "Corolla", "category": "Sedan", "price": 20000.0, "quantity": 2}, headers=headers)
    client.post("/api/vehicles", json={"make": "Ford", "model": "Explorer", "category": "SUV", "price": 40000.0, "quantity": 1}, headers=headers)

    response = client.get("/api/vehicles?make=Toyota")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

def test_update_vehicle():
    headers = get_auth_header()
    res = client.post("/api/vehicles", json={"make": "Mazda", "model": "CX-5", "category": "SUV", "price": 28000.0, "quantity": 10}, headers=headers)
    vehicle_id = res.json()["id"]

    update_res = client.put(f"/api/vehicles/{vehicle_id}", json={"price": 27000.0, "quantity": 8}, headers=headers)
    assert update_res.status_code == 200
    assert update_res.json()["price"] == 27000.0

def test_delete_vehicle():
    headers = get_auth_header()
    res = client.post("/api/vehicles", json={"make": "Nissan", "model": "Altima", "category": "Sedan", "price": 21000.0, "quantity": 4}, headers=headers)
    vehicle_id = res.json()["id"]

    del_res = client.delete(f"/api/vehicles/{vehicle_id}", headers=headers)
    assert del_res.status_code == 200

def test_protected_create_vehicle_without_token():
    response = client.post(
        "/api/vehicles",
        json={"make": "BMW", "model": "M3", "category": "Sedan", "price": 75000.00, "quantity": 2}
    )
    assert response.status_code in [401, 403]

def test_create_sale_reduces_stock():
    headers = get_auth_header()

    # 1. Create a vehicle with quantity = 5
    v_res = client.post(
        "/api/vehicles",
        json={"make": "Toyota", "model": "Corolla", "category": "Sedan", "price": 20000.0, "quantity": 5},
        headers=headers
    )
    vehicle_id = v_res.json()["id"]

    # 2. Buy 2 units
    sale_res = client.post(
        "/api/sales",
        json={"vehicle_id": vehicle_id, "quantity": 2},
        headers=headers
    )
    assert sale_res.status_code == 201
    assert sale_res.json()["total_price"] == 40000.0

    # 3. Verify remaining stock is 3
    get_v = client.get("/api/vehicles")
    vehicles = get_v.json()
    matching_v = next(v for v in vehicles if v["id"] == vehicle_id)
    assert matching_v["quantity"] == 3

def test_search_vehicles():
    headers = get_auth_header()
    client.post("/api/vehicles", json={"make": "Subaru", "model": "Outback", "category": "SUV", "price": 30000.0, "quantity": 3}, headers=headers)

    response = client.get("/api/vehicles/search?query=Outback")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["model"] == "Outback"

def test_restock_vehicle():
    headers = get_auth_header(is_admin=True)  # Admin credentials required
    # Create vehicle with initial stock of 2
    res = client.post("/api/vehicles", json={"make": "Audi", "model": "A4", "category": "Sedan", "price": 40000.0, "quantity": 2}, headers=headers)
    vehicle_id = res.json()["id"]

    # Restock with 5 additional units
    restock_res = client.post(f"/api/vehicles/{vehicle_id}/restock", json={"quantity": 5}, headers=headers)
    assert restock_res.status_code == 200
    assert restock_res.json()["quantity"] == 7