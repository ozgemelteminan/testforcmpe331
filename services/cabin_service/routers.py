from fastapi import APIRouter, Depends
from .database import SessionLocal
from . import schemas, crud, models
from services.auth.deps import get_current_user, get_current_admin_user

router = APIRouter()

@router.post('/', response_model=schemas.AttendantOut, dependencies=[Depends(get_current_admin_user)])
def create_attendant(att: schemas.AttendantCreate):
    db = SessionLocal()
    res = crud.create_attendant(db, att)
    db.close()
    return res

@router.get('/', response_model=list[schemas.AttendantOut], dependencies=[Depends(get_current_user)])
def list_att():
    db = SessionLocal()
    res = crud.list_attendants(db)
    db.close()
    return res
