from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, SessionLocal
from app.models import Vehicle
from app.routers import auth, vehicles

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Car Dealership Inventory API")

# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event to populate 10 default cars if empty
@app.on_event("startup")
def seed_default_inventory():
    db = SessionLocal()
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
    db.close()

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(vehicles.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to the Car Dealership API"}