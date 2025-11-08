
from fastapi import APIRouter, Depends, HTTPException
from ..main import SessionLocal
from ..models import Flight
from pydantic import BaseModel
from sqlalchemy.orm import Session

router = APIRouter()

class FlightIn(BaseModel):
    flight_number: str
    distance_km: int = 0
    vehicle: str = "A320"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", status_code=201)
def create_flight(f: FlightIn, db: Session = Depends(get_db)):
    if db.query(Flight).filter(Flight.flight_number == f.flight_number).first():
        raise HTTPException(400, "exists")
    db_f = Flight(flight_number=f.flight_number, distance_km=f.distance_km, vehicle=f.vehicle)
    db.add(db_f); db.commit()
    return {"ok": True, "flight": {"flight_number": f.flight_number}}

@router.get("/{flight_number}")
def get_flight(flight_number: str, db: Session = Depends(get_db)):
    f = db.query(Flight).filter(Flight.flight_number == flight_number).first()
    if not f:
        raise HTTPException(404, "not found")
    return f
