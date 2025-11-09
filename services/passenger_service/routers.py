from fastapi import APIRouter, Depends
from .database import SessionLocal
from . import schemas, crud
# DÜZELTME: Admin kontrol fonksiyonu import edildi
from services.auth.deps import get_current_user, get_current_admin_user

router = APIRouter()

# DÜZELTME: dependencies=[Depends(get_current_admin_user)] olarak değiştirildi
# Artık sadece admin rolüne sahip olanlar yeni yolcu ekleyebilir.
@router.post('/', response_model=schemas.PassengerOut, dependencies=[Depends(get_current_admin_user)])
def create_passenger(p: schemas.PassengerCreate):
    db = SessionLocal()
    res = crud.create_passenger(db, p)
    db.close()
    return res

# GET (listeleme) endpoint'i 'get_current_user' olarak kalır.
# (Token'ı olan herkes yolcuları listeleyebilir)
@router.get('/', response_model=list[schemas.PassengerOut], dependencies=[Depends(get_current_user)])
def list_passengers():
    db = SessionLocal()
    res = crud.list_passengers(db)
    db.close()
    return res
