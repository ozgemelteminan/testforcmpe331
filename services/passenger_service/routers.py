from fastapi import APIRouter, Depends, HTTPException, Query # Query ve HTTPException EKLENDİ
from sqlalchemy.orm import Session # Session EKLENDİ
from .database import SessionLocal
from . import schemas, crud
from services.auth.deps import get_current_user, get_current_admin_user
from typing import List, Optional # EKLENDİ

router = APIRouter()

# POST (Admin Yetkisi) - (Değişiklik yok)
@router.post('/', response_model=schemas.PassengerOut, dependencies=[Depends(get_current_admin_user)])
def create_passenger(p: schemas.PassengerCreate):
    db = SessionLocal()
    res = crud.create_passenger(db, p)
    db.close()
    return res

# GET (Listeleme) - FİLTRELEME EKLENDİ
@router.get('/', response_model=list[schemas.PassengerOut], dependencies=[Depends(get_current_user)])
def list_passengers(
    # EKLENDİ: Arkadaşının PDF'indeki gibi filtreleme parametreleri
    flight: Optional[str] = Query(None, description="Filter by flight_id"),
    seat_type: Optional[str] = Query(None, description="Filter by seat_type: business or economy"),
    skip: int = 0,
    limit: int = 100
):
    db = SessionLocal()
    res = crud.list_passengers(
        db,
        flight_id=flight,
        seat_type=seat_type,
        skip=skip,
        limit=limit
    )
    db.close()
    return res

# --- YENİ ENDPOINT'LER EKLENDİ ---

# GET (ID ile Detay Getirme)
@router.get('/{passenger_id}', response_model=schemas.PassengerOut, dependencies=[Depends(get_current_user)])
def get_passenger_detail(passenger_id: int):
    db = SessionLocal()
    db_passenger = crud.get_passenger_by_id(db, passenger_id=passenger_id)
    db.close()
    if db_passenger is None:
        raise HTTPException(status_code=404, detail="Passenger not found")
    return db_passenger

# PUT (Güncelleme - Admin Yetkisi)
@router.put('/{passenger_id}', response_model=schemas.PassengerOut, dependencies=[Depends(get_current_admin_user)])
def update_passenger_detail(passenger_id: int, p_update: schemas.PassengerBase):
    db = SessionLocal()
    updated_passenger = crud.update_passenger(db, passenger_id=passenger_id, p_update=p_update)
    db.close()
    if updated_passenger is None:
        raise HTTPException(status_code=404, detail="Passenger not found")
    return updated_passenger

# DELETE (Silme - Admin Yetkisi)
@router.delete('/{passenger_id}', response_model=schemas.PassengerOut, dependencies=[Depends(get_current_admin_user)])
def delete_passenger_record(passenger_id: int):
    db = SessionLocal()
    deleted_passenger = crud.delete_passenger(db, passenger_id=passenger_id)
    db.close()
    if deleted_passenger is None:
        raise HTTPException(status_code=404, detail="Passenger not found")
    return deleted_passenger
