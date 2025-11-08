from sqlalchemy.orm import Session
from . import models, schemas

def create_pilot(db: Session, pilot: schemas.PilotCreate):
    db_p = models.Pilot(**pilot.dict())
    db.add(db_p)
    db.commit()
    db.refresh(db_p)
    return db_p

def get_pilot(db: Session, pilot_id: int):
    return db.query(models.Pilot).filter(models.Pilot.id==pilot_id).first()

def list_pilots(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Pilot).offset(skip).limit(limit).all()
