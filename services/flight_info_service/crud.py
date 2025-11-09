from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional
import datetime # EKLENDİ

# --- Flight CRUD ---
def create_flight(db: Session, f: schemas.FlightCreate):
    flight_data = f.dict()
    db_f = models.Flight(**flight_data)
    db.add(db_f)
    db.commit()
    db.refresh(db_f)
    return db_f

# EKLENDİ
def get_flight_by_id(db: Session, flight_id: int):
    return db.query(models.Flight).filter(models.Flight.id == flight_id).first()
    
# EKLENDİ (Arkadaşınınki flight_number ile alıyor)
def get_flight_by_flight_number(db: Session, flight_number: str):
    return db.query(models.Flight).filter(models.Flight.flight_number == flight_number).first()

# DÜZELTME: list_flights (Filtreleme eklendi)
def list_flights(
    db: Session,
    vehicle_type: Optional[str] = None,
    departure_time_date: Optional[datetime.date] = None, # Arkadaşının dökümanındaki gibi
    skip: int = 0,
    limit: int = 100
):
    query = db.query(models.Flight)
    
    if vehicle_type:
        query = query.filter(models.Flight.vehicle_type == vehicle_type)
    
    if departure_time_date:
        # Sadece tarihe göre filtrele (datetime objesini string'e çevirip karşılaştır)
        # Not: Bu sorgu SQLite'ta çalışır, PostgreSQL için `::date` gerekebilir
        query = query.filter(models.Flight.datetime.like(f"{departure_time_date.isoformat()}%"))
            
    return query.offset(skip).limit(limit).all()

# EKLENDİ
def update_flight(db: Session, flight_id: int, f_update: schemas.FlightBase):
    db_flight = get_flight_by_id(db, flight_id)
    if not db_flight:
        return None
    
    update_data = f_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_flight, key, value)
        
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight

# EKLENDİ
def delete_flight(db: Session, flight_id: int):
    db_flight = get_flight_by_id(db, flight_id)
    if not db_flight:
        return None
    
    db.delete(db_flight)
    db.commit()
    return db_flight

# --- Airport CRUD (Değişiklik yok) ---
def create_airport(db: Session, airport: schemas.AirportCreate):
    db_airport = models.Airport(**airport.dict())
    db.add(db_airport)
    db.commit()
    db.refresh(db_airport)
    return db_airport

def list_airports(db: Session, skip=0, limit=100):
    return db.query(models.Airport).offset(skip).limit(limit).all()

# --- VehicleType CRUD (Değişiklik yok) ---
def create_vehicle_type(db: Session, vehicle: schemas.VehicleTypeCreate):
    db_vehicle = models.VehicleType(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def list_vehicle_types(db: Session, skip=0, limit=100):
    return db.query(models.VehicleType).offset(skip).limit(limit).all()
