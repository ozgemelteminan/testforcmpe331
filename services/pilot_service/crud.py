from sqlalchemy.orm import Session
from . import models, schemas
from typing import Optional # EKLENDİ

def create_pilot(db: Session, pilot: schemas.PilotCreate):
    db_p = models.Pilot(**pilot.dict())
    db.add(db_p)
    db.commit()
    db.refresh(db_p)
    return db_p

# DÜZELTME: Fonksiyon adı daha net hale getirildi
def get_pilot_by_id(db: Session, pilot_id: int):
    return db.query(models.Pilot).filter(models.Pilot.id == pilot_id).first()

# DÜZELTME: list_pilots artık filtreleme parametreleri alıyor
def list_pilots(
    db: Session,
    seniority: Optional[str] = None,
    vehicle_restriction: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    query = db.query(models.Pilot)
    
    # EKLENDİ: Kıdeme (seniority) göre filtrele
    if seniority:
        query = query.filter(models.Pilot.seniority == seniority)
        
    # EKLENDİ: Araç kısıtlamasına göre filtrele
    if vehicle_restriction:
        query = query.filter(models.Pilot.vehicle_restriction == vehicle_restriction)
        
    return query.offset(skip).limit(limit).all()

# --- YENİ FONKSİYONLAR EKLENDİ ---

def update_pilot(db: Session, pilot_id: int, pilot_update: schemas.PilotBase):
    db_pilot = get_pilot_by_id(db, pilot_id)
    if not db_pilot:
        return None
    
    # Gelen veriyi modele dök (None olanları hariç tut)
    update_data = pilot_update.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_pilot, key, value)
        
    db.add(db_pilot)
    db.commit()
    db.refresh(db_pilot)
    return db_pilot

def delete_pilot(db: Session, pilot_id: int):
    db_pilot = get_pilot_by_id(db, pilot_id)
    if not db_pilot:
        return None
    
    db.delete(db_pilot)
    db.commit()
    return db_pilot
