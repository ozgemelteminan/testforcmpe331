from sqlalchemy.orm import Session
from . import models, schemas
def create_passenger(db: Session, p: schemas.PassengerCreate):
    db_p = models.Passenger(**p.dict())
    db.add(db_p)
    db.commit()
    db.refresh(db_p)
    return db_p
def list_passengers(db: Session, skip=0, limit=100):
    return db.query(models.Passenger).offset(skip).limit(limit).all()
