from sqlalchemy.orm import Session
from . import models, schemas
def create_flight(db: Session, f: schemas.FlightCreate):
    db_f = models.Flight(**f.dict())
    db.add(db_f)
    db.commit()
    db.refresh(db_f)
    return db_f
def list_flights(db: Session, skip=0, limit=100):
    return db.query(models.Flight).offset(skip).limit(limit).all()
