from fastapi import APIRouter, Depends, HTTPException, Query # EKLENDİ
from sqlalchemy.orm import Session # EKLENDİ
from .database import SessionLocal
from . import schemas, crud
from services.auth.deps import get_current_user, get_current_admin_user
from typing import List, Optional # EKLENDİ
import datetime # EKLENDİ

router = APIRouter()

# --- Flight Endpoint'leri ---

@router.post('/flights/', response_model=schemas.FlightOut, dependencies=[Depends(get_current_admin_user)])
def create_flight(f: schemas.FlightCreate):
    db = SessionLocal()
    # flight_number'ın unique olduğundan emin ol
    db_flight = crud.get_flight_by_flight_number(db, f.flight_number)
    if db_flight:
        raise HTTPException(status_code=400, detail="Flight number already registered")
    res = crud.create_flight(db, f)
    db.close()
    return res

# DÜZELTME: GET (Listeleme) Filtreleme eklendi
@router.get('/flights/', response_model=List[schemas.FlightOut], dependencies=[Depends(get_current_user)])
def list_flights(
    # EKLENDİ: Arkadaşının PDF'indeki gibi filtreleme
    vehicle_type: Optional[str] = Query(None, description="Filter by vehicle_type (e.g., A320)"),
    departure_time_date: Optional[datetime.date] = Query(None, description="Filter by departure date (YYYY-MM-DD)"),
    skip: int = 0,
    limit: int = 100
):
    db = SessionLocal()
    res = crud.list_flights(
        db,
        vehicle_type=vehicle_type,
        departure_time_date=departure_time_date,
        skip=skip,
        limit=limit
    )
    db.close()
    return res

# EKLENDİ: GET (ID ile Detay Getirme)
@router.get('/flights/{flight_id}', response_model=schemas.FlightOut, dependencies=[Depends(get_current_user)])
def get_flight_detail(flight_id: int):
    db = SessionLocal()
    db_flight = crud.get_flight_by_id(db, flight_id=flight_id)
    db.close()
    if db_flight is None:
        raise HTTPException(status_code=404, detail="Flight not found")
    return db_flight
    
# EKLENDİ: PUT (Güncelleme - Admin Yetkisi)
@router.put('/flights/{flight_id}', response_model=schemas.FlightOut, dependencies=[Depends(get_current_admin_user)])
def update_flight_detail(flight_id: int, f_update: schemas.FlightBase):
    db = SessionLocal()
    updated_flight = crud.update_flight(db, flight_id=flight_id, f_update=f_update)
    db.close()
    if updated_flight is None:
        raise HTTPException(status_code=404, detail="Flight not found")
    return updated_flight

# EKLENDİ: DELETE (Silme - Admin Yetkisi)
@router.delete('/flights/{flight_id}', response_model=schemas.FlightOut, dependencies=[Depends(get_current_admin_user)])
def delete_flight_record(flight_id: int):
    db = SessionLocal()
    deleted_flight = crud.delete_flight(db, flight_id=flight_id)
    db.close()
    if deleted_flight is None:
        raise HTTPException(status_code=404, detail="Flight not found")
    return deleted_flight


# --- Airport Endpoint'leri (Değişiklik yok) ---
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
    
# --- Vehicle Types Endpoint'leri (Değişiklik yok) ---
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
