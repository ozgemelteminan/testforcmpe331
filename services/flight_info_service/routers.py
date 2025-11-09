from fastapi import APIRouter, Depends
from .database import SessionLocal
from . import schemas, crud
# DÜZELTME: Admin kontrol fonksiyonu import edildi
from services.auth.deps import get_current_user, get_current_admin_user
from typing import List # EKLENDİ

router = APIRouter()

# --- Flight Endpoint'leri ---

@router.post('/flights/', response_model=schemas.FlightOut, dependencies=[Depends(get_current_admin_user)])
def create_flight(f: schemas.FlightCreate):
    db = SessionLocal()
    res = crud.create_flight(db, f)
    db.close()
    return res

@router.get('/flights/', response_model=List[schemas.FlightOut], dependencies=[Depends(get_current_user)])
def list_flights():
    db = SessionLocal()
    res = crud.list_flights(db)
    db.close()
    return res

# --- YENİ EKLENDİ: Airport Endpoint'leri (Arkadaşının  API'si gibi) ---

@router.post('/airports/', response_model=schemas.AirportOut, dependencies=[Depends(get_current_admin_user)])
def create_airport(airport: schemas.AirportCreate):
    db = SessionLocal()
    res = crud.create_airport(db, airport)
    db.close()
    return res

@router.get('/airports/', response_model=List[schemas.AirportOut], dependencies=[Depends(get_current_user)])
def list_airports():
    db = SessionLocal()
    res = crud.list_airports(db)
    db.close()
    return res
    
# --- YENİ EKLENDİ: Vehicle Types Endpoint'leri (Arkadaşının  API'si gibi) ---

@router.post('/vehicle-types/', response_model=schemas.VehicleTypeOut, dependencies=[Depends(get_current_admin_user)])
def create_vehicle_type(vehicle: schemas.VehicleTypeCreate):
    db = SessionLocal()
    res = crud.create_vehicle_type(db, vehicle)
    db.close()
    return res

@router.get('/vehicle-types/', response_model=List[schemas.VehicleTypeOut], dependencies=[Depends(get_current_user)])
def list_vehicle_types():
    db = SessionLocal()
    res = crud.list_vehicle_types(db)
    db.close()
    return res
