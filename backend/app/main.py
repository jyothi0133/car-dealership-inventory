import jwt
from typing import List, Optional
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import engine, Base, get_db
from app.models import User, Vehicle, Sale, SaleCreate, SaleResponse, RestockCreate

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "supersecretkey_that_is_at_least_32_bytes_long"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Security Dependency ---
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return user


def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if not getattr(current_user, 'is_admin', False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Admin privileges required"
        )
    return current_user


# --- Auth Schemas ---
class RegisterSchema(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None

class LoginSchema(BaseModel):
    email: EmailStr
    password: str


# --- Vehicle Schemas ---
class VehicleCreateSchema(BaseModel):
    make: str
    model: str
    category: str
    price: float
    quantity: int

class VehicleResponseSchema(VehicleCreateSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)

class VehicleUpdateSchema(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None


# --- Auth Endpoints ---
@app.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
def register(user: RegisterSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    username = user.username or user.email.split("@")[0]
    hashed_password = pwd_context.hash(user.password)
    new_user = User(
        username=username,
        email=user.email,
        password_hash=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "username": new_user.username,
        "email": new_user.email
    }

@app.post("/api/auth/login", status_code=status.HTTP_200_OK)
def login(credentials: LoginSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == credentials.email).first()
    if not db_user or not pwd_context.verify(credentials.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    payload = {
        "sub": db_user.email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=2)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {
        "access_token": token,
        "token_type": "bearer"
    }


# --- Vehicle Endpoints ---
@app.get("/api/vehicles/search", response_model=List[VehicleResponseSchema], status_code=status.HTTP_200_OK)
def search_vehicles(
    query: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    q = db.query(Vehicle)
    if query:
        q = q.filter(
            (Vehicle.make.ilike(f"%{query}%")) |
            (Vehicle.model.ilike(f"%{query}%")) |
            (Vehicle.category.ilike(f"%{query}%"))
        )
    if min_price is not None:
        q = q.filter(Vehicle.price >= min_price)
    if max_price is not None:
        q = q.filter(Vehicle.price <= max_price)
    
    return q.all()

@app.post("/api/vehicles", response_model=VehicleResponseSchema, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    vehicle: VehicleCreateSchema, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Use get_current_user instead of get_current_admin_user
):
    new_vehicle = Vehicle(**vehicle.model_dump())
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle

@app.get("/api/vehicles", response_model=List[VehicleResponseSchema], status_code=status.HTTP_200_OK)
def get_vehicles(
    make: Optional[str] = None,
    category: Optional[str] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Vehicle)
    if make:
        query = query.filter(Vehicle.make.ilike(f"%{make}%"))
    if category:
        query = query.filter(Vehicle.category.ilike(f"%{category}%"))
    if max_price is not None:
        query = query.filter(Vehicle.price <= max_price)
    
    return query.all()

@app.put("/api/vehicles/{vehicle_id}", response_model=VehicleResponseSchema, status_code=status.HTTP_200_OK)
def update_vehicle(
    vehicle_id: int, 
    vehicle_update: VehicleUpdateSchema, 
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not db_vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    
    update_data = vehicle_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_vehicle, key, value)
        
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@app.delete("/api/vehicles/{vehicle_id}", status_code=status.HTTP_200_OK)
def delete_vehicle(
    vehicle_id: int, 
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not db_vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    
    db.delete(db_vehicle)
    db.commit()
    return {"message": "Vehicle deleted successfully"}


# --- Sales & Purchase Endpoints ---
@app.post("/api/sales", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def create_sale(
    sale_data: SaleCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vehicle = db.query(Vehicle).filter(Vehicle.id == sale_data.vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Vehicle not found"
        )

    if vehicle.quantity < sale_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock. Available: {vehicle.quantity}"
        )

    vehicle.quantity -= sale_data.quantity
    calculated_total = vehicle.price * sale_data.quantity

    new_sale = Sale(
        vehicle_id=vehicle.id,
        user_id=current_user.id,
        quantity=sale_data.quantity,
        total_price=calculated_total
    )

    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)

    return new_sale

@app.post("/api/vehicles/{vehicle_id}/purchase", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def purchase_vehicle(
    vehicle_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sale_data = SaleCreate(vehicle_id=vehicle_id, quantity=1)
    return create_sale(sale_data=sale_data, db=db, current_user=current_user)


# --- Restock Endpoint (Admin Only) ---
@app.post("/api/vehicles/{vehicle_id}/restock", response_model=VehicleResponseSchema, status_code=status.HTTP_200_OK)
def restock_vehicle(
    vehicle_id: int,
    restock_data: RestockCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    if restock_data.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Restock quantity must be greater than zero"
        )
        
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
        
    vehicle.quantity += restock_data.quantity
    db.commit()
    db.refresh(vehicle)
    return vehicle