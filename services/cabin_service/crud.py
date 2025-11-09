from sqlalchemy.orm import Session
from . import models, schemas
from typing import Optional # EKLENDİ

def create_attendant(db: Session, att: schemas.AttendantCreate):
    db_a = models.Attendant(**att.dict())
    db.add(db_a)
    db.commit()
    db.refresh(db_a)
    return db_a

# --- YENİ EKLENDİ ---
def get_attendant_by_id(db: Session, attendant_id: int):
    return db.query(models.Attendant).filter(models.Attendant.id == attendant_id).first()

# DÜZELTME: list_attendants artık filtreleme alıyor
def list_attendants(
    db: Session,
    attendant_type: Optional[str] = None,
    seniority: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    query = db.query(models.Attendant)
    
    # EKLENDİ: Arkadaşının PDF'indeki gibi filtreleme
    if attendant_type:
        query = query.filter(models.Attendant.attendant_type == attendant_type)
    if seniority:
        query = query.filter(models.Attendant.seniority == seniority)
        
    return query.offset(skip).limit(limit).all()

# --- YENİ EKLENDİ ---
def update_attendant(db: Session, attendant_id: int, att_update: schemas.AttendantBase):
    db_att = get_attendant_by_id(db, attendant_id)
    if not db_att:
        return None
    
    update_data = att_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_att, key, value)
        
    db.add(db_att)
    db.commit()
    db.refresh(db_att)
    return db_att

# --- YENİ EKLENDİ ---
def delete_attendant(db: Session, attendant_id: int):
    db_att = get_attendant_by_id(db, attendant_id)
    if not db_att:
        return None
    
    db.delete(db_att)
    db.commit()
    return db_att
