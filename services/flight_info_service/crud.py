from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional # EKLENDİ

# ... (Mevcut create_flight ve list_flights kodları burada) ...
def create_flight(db: Session, f: schemas.FlightCreate):
    # DİKKAT: Bu kod, FlightBase'deki LocationDetail objesini
    # Flight modelindeki JSON alanına düzgünce kaydetmek için
    # dict() çağrısına ihtiyaç duyar.
    flight_data = f.dict()
    db_f = models.Flight(**flight_data)
    db.add(db_f)
    db.commit()
    db.refresh(db_f)
    return db_f

def list_flights(db: Session, skip=0, limit=100):
    return db.query(models.Flight).offset(skip).limit(limit).all()

# --- YENİ EKLENDİ: Airport CRUD Fonksiyonları ---

def create_airport(db: Session, airport: schemas.AirportCreate):
    db_airport = models.Airport(**airport.dict())
    db.add(db_airport)
    db.commit()
    db.refresh(db_airport)
    return db_airport

def list_airports(db: Session, skip=0, limit=100):
    return db.query(models.Airport).offset(skip).limit(limit).all()

# --- YENİ EKLENDİ: VehicleType CRUD Fonksiyonları ---

def create_vehicle_type(db: Session, vehicle: schemas.VehicleTypeCreate):
    db_vehicle = models.VehicleType(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def list_vehicle_types(db: Session, skip=0, limit=100):
    return db.query(models.VehicleType).offset(skip).limit(limit).all()
