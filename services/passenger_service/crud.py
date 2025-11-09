from sqlalchemy.orm import Session
from . import models, schemas
from typing import Optional # EKLENDİ

def create_passenger(db: Session, p: schemas.PassengerCreate):
    db_p = models.Passenger(**p.dict())
    db.add(db_p)
    db.commit()
    db.refresh(db_p)
    return db_p

# --- YENİ FONKSİYON EKLENDİ ---
def get_passenger_by_id(db: Session, passenger_id: int):
    return db.query(models.Passenger).filter(models.Passenger.id == passenger_id).first()

# DÜZELTME: list_passengers artık filtreleme parametreleri alıyor
def list_passengers(
    db: Session,
    flight_id: Optional[str] = None,
    seat_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    query = db.query(models.Passenger)
    
    # EKLENDİ: Uçuş ID'sine göre filtrele
    if flight_id:
        query = query.filter(models.Passenger.flight_id == flight_id)
        
    # EKLENDİ: Koltuk tipine göre filtrele
    if seat_type:
        query = query.filter(models.Passenger.seat_type == seat_type)
        
    return query.offset(skip).limit(limit).all()

# --- YENİ FONKSİYONLAR EKLENDİ ---

def update_passenger(db: Session, passenger_id: int, p_update: schemas.PassengerBase):
    db_passenger = get_passenger_by_id(db, passenger_id)
    if not db_passenger:
        return None
    
    update_data = p_update.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_passenger, key, value)
        
    db.add(db_passenger)
    db.commit()
    db.refresh(db_passenger)
    return db_passenger

def delete_passenger(db: Session, passenger_id: int):
    db_passenger = get_passenger_by_id(db, passenger_id)
    if not db_passenger:
        return None
    
    db.delete(db_passenger)
    db.commit()
    return db_passenger
