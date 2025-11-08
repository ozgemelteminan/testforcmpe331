from sqlalchemy.orm import Session
from . import models, schemas
def create_attendant(db: Session, att: schemas.AttendantCreate):
    db_a = models.Attendant(**att.dict())
    db.add(db_a)
    db.commit()
    db.refresh(db_a)
    return db_a
def list_attendants(db: Session, skip=0, limit=100):
    return db.query(models.Attendant).offset(skip).limit(limit).all()
