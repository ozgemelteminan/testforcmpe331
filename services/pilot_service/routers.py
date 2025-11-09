from fastapi import APIRouter, Depends, HTTPException, Query # Query EKLENDİ
from sqlalchemy.orm import Session
from . import crud, schemas, models
from .database import SessionLocal, engine
from services.auth.deps import get_current_user, get_current_admin_user
from typing import List, Optional # EKLENDİ

router = APIRouter()
models.Base = getattr(models, 'Base', None)

# POST (Admin Yetkisi)
@router.post('/', response_model=schemas.PilotOut, dependencies=[Depends(get_current_admin_user)])
def create(p: schemas.PilotCreate):
    db = SessionLocal()
    res = crud.create_pilot(db, p)
    db.close()
    return res

# GET (Listeleme) - FİLTRELEME EKLENDİ
@router.get('/', response_model=list[schemas.PilotOut], dependencies=[Depends(get_current_user)])
def list_all(
    # EKLENDİ: Arkadaşının PDF'indeki gibi filtreleme parametreleri
    seniority: Optional[str] = Query(None, description="Filter by seniority: senior, junior, trainee"),
    vehicle_restriction: Optional[str] = Query(None, description="Filter by vehicle restriction (e.g., A320)"),
    skip: int = 0,
    limit: int = 100
):
    db = SessionLocal()
    res = crud.list_pilots(
        db,
        seniority=seniority,
        vehicle_restriction=vehicle_restriction,
        skip=skip,
        limit=limit
    )
    db.close()
    return res

# --- YENİ ENDPOINT'LER EKLENDİ ---

# GET (ID ile Detay Getirme)
@router.get('/{pilot_id}', response_model=schemas.PilotOut, dependencies=[Depends(get_current_user)])
def get_pilot_detail(pilot_id: int):
    db = SessionLocal()
    db_pilot = crud.get_pilot_by_id(db, pilot_id=pilot_id)
    db.close()
    if db_pilot is None:
        raise HTTPException(status_code=404, detail="Pilot not found")
    return db_pilot

# PUT (Güncelleme - Admin Yetkisi)
@router.put('/{pilot_id}', response_model=schemas.PilotOut, dependencies=[Depends(get_current_admin_user)])
def update_pilot_detail(pilot_id: int, pilot_update: schemas.PilotBase):
    db = SessionLocal()
    updated_pilot = crud.update_pilot(db, pilot_id=pilot_id, pilot_update=pilot_update)
    db.close()
    if updated_pilot is None:
        raise HTTPException(status_code=404, detail="Pilot not found")
    return updated_pilot

# DELETE (Silme - Admin Yetkisi)
@router.delete('/{pilot_id}', response_model=schemas.PilotOut, dependencies=[Depends(get_current_admin_user)])
def delete_pilot_record(pilot_id: int):
    db = SessionLocal()
    deleted_pilot = crud.delete_pilot(db, pilot_id=pilot_id)
    db.close()
    if deleted_pilot is None:
        raise HTTPException(status_code=404, detail="Pilot not found")
    return deleted_pilot
