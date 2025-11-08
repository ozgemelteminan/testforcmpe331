from fastapi import APIRouter, Depends
from .database import SessionLocal
from . import schemas, crud
from services.auth.deps import get_current_user

router = APIRouter()
@router.post('/', response_model=schemas.FlightOut, dependencies=[Depends(get_current_user)])
def create_flight(f: schemas.FlightCreate):
    db = SessionLocal()
    res = crud.create_flight(db, f)
    db.close()
    return res
@router.get('/', response_model=list[schemas.FlightOut], dependencies=[Depends(get_current_user)])
def list_flights():
    db = SessionLocal()
    res = crud.list_flights(db)
    db.close()
    return res
