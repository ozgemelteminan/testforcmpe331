from fastapi import APIRouter, Depends, HTTPException, Query # EKLENDİ
from sqlalchemy.orm import Session # EKLENDİ
from .database import SessionLocal
from . import schemas, crud, models
from services.auth.deps import get_current_user, get_current_admin_user
from typing import List, Optional # EKLENDİ

router = APIRouter()

@router.post('/', response_model=schemas.AttendantOut, dependencies=[Depends(get_current_admin_user)])
def create_attendant(att: schemas.AttendantCreate):
    db = SessionLocal()
    res = crud.create_attendant(db, att)
    db.close()
    return res

# DÜZELTME: GET (Listeleme) Filtreleme eklendi
@router.get('/', response_model=list[schemas.AttendantOut], dependencies=[Depends(get_current_user)])
def list_att(
    # EKLENDİ: Arkadaşının PDF'indeki gibi filtreleme
    attendant_type: Optional[str] = Query(None, description="Filter by type: chief, regular, chef"),
    seniority: Optional[str] = Query(None, description="Filter by seniority: senior, junior"),
    skip: int = 0,
    limit: int = 100
):
    db = SessionLocal()
    res = crud.list_attendants(
        db,
        attendant_type=attendant_type,
        seniority=seniority,
        skip=skip,
        limit=limit
    )
    db.close()
    return res

# --- YENİ EKLENDİ: ID ile Detay Getirme ---
@router.get('/{attendant_id}', response_model=schemas.AttendantOut, dependencies=[Depends(get_current_user)])
def get_attendant_detail(attendant_id: int):
    db = SessionLocal()
    db_att = crud.get_attendant_by_id(db, attendant_id=attendant_id)
    db.close()
    if db_att is None:
        raise HTTPException(status_code=404, detail="Attendant not found")
    return db_att

# --- YENİ EKLENDİ: PUT (Güncelleme - Admin Yetkisi) ---
@router.put('/{attendant_id}', response_model=schemas.AttendantOut, dependencies=[Depends(get_current_admin_user)])
def update_attendant_detail(attendant_id: int, att_update: schemas.AttendantBase):
    db = SessionLocal()
    updated_att = crud.update_attendant(db, attendant_id=attendant_id, att_update=att_update)
    db.close()
    if updated_att is None:
        raise HTTPException(status_code=404, detail="Attendant not found")
    return updated_att

# --- YENİ EKLENDİ: DELETE (Silme - Admin Yetkisi) ---
@router.delete('/{attendant_id}', response_model=schemas.AttendantOut, dependencies=[Depends(get_current_admin_user)])
def delete_attendant_record(attendant_id: int):
    db = SessionLocal()
    deleted_att = crud.delete_attendant(db, attendant_id=attendant_id)
    db.close()
    if deleted_att is None:
        raise HTTPException(status_code=404, detail="Attendant not found")
    return deleted_att
