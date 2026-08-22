from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .database import engine, Base, SessionLocal
from .models import Vehicle

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Car Dealership Inventory API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VehicleCreate(BaseModel):
    make: str
    model: str
    category: str
    price: float
    quantity: int

@app.on_event("startup")
def seed_default_inventory():
    db = SessionLocal()
    try:
        if db.query(Vehicle).count() == 0:
            default_cars = [
                Vehicle(make="Toyota", model="Camry", category="Sedan", price=26000.0, quantity=5),
                Vehicle(make="Toyota", model="RAV4", category="SUV", price=30000.0, quantity=4),
                Vehicle(make="Audi", model="A4", category="Sedan", price=41000.0, quantity=3),
                Vehicle(make="Audi", model="Q5", category="SUV", price=45000.0, quantity=2),
                Vehicle(make="BMW", model="3 Series", category="Sedan", price=44000.0, quantity=3),
                Vehicle(make="BMW", model="X5", category="SUV", price=65000.0, quantity=2),
                Vehicle(make="Honda", model="Civic", category="Sedan", price=24000.0, quantity=6),
                Vehicle(make="Honda", model="CR-V", category="SUV", price=29000.0, quantity=5),
                Vehicle(make="Ford", model="Mustang", category="Coupe", price=38000.0, quantity=2),
                Vehicle(make="Tesla", model="Model 3", category="Electric", price=39000.0, quantity=4),
            ]
            db.add_all(default_cars)
            db.commit()
    finally:
        db.close()

# 1. Get all vehicles
@app.get("/api/vehicles")
def get_vehicles():
    db = SessionLocal()
    try:
        return db.query(Vehicle).all()
    finally:
        db.close()

# 2. Add new vehicle
@app.post("/api/vehicles")
def create_vehicle(vehicle: VehicleCreate):
    db = SessionLocal()
    try:
        new_car = Vehicle(**vehicle.dict())
        db.add(new_car)
        db.commit()
        db.refresh(new_car)
        return new_car
    finally:
        db.close()

# 3. Buy vehicle (Decrease quantity)
@app.post("/api/vehicles/{vehicle_id}/buy")
def buy_vehicle(vehicle_id: int):
    db = SessionLocal()
    try:
        car = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not car:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        if car.quantity <= 0:
            raise HTTPException(status_code=400, detail="Out of stock")
        car.quantity -= 1
        db.commit()
        return car
    finally:
        db.close()

# 4. Restock vehicle (Increase quantity)
@app.post("/api/vehicles/{vehicle_id}/restock")
def restock_vehicle(vehicle_id: int):
    db = SessionLocal()
    try:
        car = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not car:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        car.quantity += 1
        db.commit()
        return car
    finally:
        db.close()

# 5. Delete vehicle
@app.delete("/api/vehicles/{vehicle_id}")
def delete_vehicle(vehicle_id: int):
    db = SessionLocal()
    try:
        car = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not car:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        db.delete(car)
        db.commit()
        return {"message": "Vehicle deleted successfully"}
    finally:
        db.close()