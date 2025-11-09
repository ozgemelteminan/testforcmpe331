from fastapi import APIRouter, Depends
from .database import SessionLocal
from . import schemas, crud
# DÜZELTME: Admin kontrol fonksiyonu import edildi
from services.auth.deps import get_current_user, get_current_admin_user

router = APIRouter()

# DÜZELTME: dependencies=[Depends(get_current_admin_user)] olarak değiştirildi
# Artık sadece admin rolüne sahip olanlar yeni uçuş ekleyebilir.
@router.post('/', response_model=schemas.FlightOut, dependencies=[Depends(get_current_admin_user)])
def create_flight(f: schemas.FlightCreate):
    db = SessionLocal()
    res = crud.create_flight(db, f)
    db.close()
    return res

# GET (listeleme) endpoint'i 'get_current_user' olarak kalır.
# (Token'ı olan herkes uçuşları listeleyebilir)
@router.get('/', response_model=list[schemas.FlightOut], dependencies=[Depends(get_current_user)])
def list_flights():
    db = SessionLocal()
    res = crud.list_flights(db)
    db.close()
    return res
