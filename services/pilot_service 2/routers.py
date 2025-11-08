from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas, models
from .database import SessionLocal, engine
from services.auth.deps import get_current_user

router = APIRouter()
models.Base = getattr(models, 'Base', None)

@router.post('/', response_model=schemas.PilotOut, dependencies=[Depends(get_current_user)])
def create(p: schemas.PilotCreate):
    db = SessionLocal()
    res = crud.create_pilot(db, p)
    db.close()
    return res

@router.get('/', response_model=list[schemas.PilotOut], dependencies=[Depends(get_current_user)])
def list_all():
    db = SessionLocal()
    res = crud.list_pilots(db)
    db.close()
    return res
