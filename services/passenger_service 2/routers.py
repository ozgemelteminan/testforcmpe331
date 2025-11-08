from fastapi import APIRouter, Depends
from .database import SessionLocal
from . import schemas, crud
from services.auth.deps import get_current_user

router = APIRouter()
@router.post('/', response_model=schemas.PassengerOut, dependencies=[Depends(get_current_user)])
def create_passenger(p: schemas.PassengerCreate):
    db = SessionLocal()
    res = crud.create_passenger(db, p)
    db.close()
    return res
@router.get('/', response_model=list[schemas.PassengerOut], dependencies=[Depends(get_current_user)])
def list_passengers():
    db = SessionLocal()
    res = crud.list_passengers(db)
    db.close()
    return res
