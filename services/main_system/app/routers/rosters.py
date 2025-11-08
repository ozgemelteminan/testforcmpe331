
from fastapi import APIRouter, HTTPException, Depends
from ..main import SessionLocal
from ..models import Flight, Roster
from sqlalchemy.orm import Session
import requests, os
from datetime import datetime

router = APIRouter()

PASSENGER_SERVICE_URL = os.getenv('PASSENGER_SERVICE_URL', 'http://localhost:8004')
PILOT_SERVICE_URL = os.getenv('PILOT_SERVICE_URL', 'http://localhost:8002')
CABIN_SERVICE_URL = os.getenv('CABIN_SERVICE_URL', 'http://localhost:8003')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def select_pilots(pool, vehicle, distance):
    # simple pick first 2 pilots that match vehicle_restriction or any
    sel = []
    for p in pool:
        if p.get('vehicle_restriction') in (vehicle, '', None):
            sel.append(p)
        if len(sel) >= 2:
            break
    return sel

def select_attendants(pool, vehicle):
    sel = []
    for a in pool:
        if vehicle in a.get('vehicle_restrictions', []) or not a.get('vehicle_restrictions'):
            sel.append(a)
        if len(sel) >= 4:
            break
    return sel

@router.post('/generate/{flight_number}')
def generate(flight_number: str, db: Session = Depends(get_db)):
    flight = db.query(Flight).filter(Flight.flight_number==flight_number).first()
    if not flight:
        raise HTTPException(404, 'flight not found')
    # get passengers
    resp = requests.get(f"{PASSENGER_SERVICE_URL}/passengers/by-flight/{flight_number}")
    if resp.status_code != 200:
        raise HTTPException(502, 'passenger service error')
    passengers = resp.json()
    pilots = requests.get(f"{PILOT_SERVICE_URL}/pilots").json()
    attendants = requests.get(f"{CABIN_SERVICE_URL}/attendants").json()
    sel_pilots = select_pilots(pilots, flight.vehicle, flight.distance_km)
    sel_att = select_attendants(attendants, flight.vehicle)
    # simple seat assignment: fill seat numbers like 1A,1B,... by passenger index
    seating = []
    rows = [f for f in range(1, 31)]
    seats = [f"{r}{c}" for r in rows for c in ['A','B','C','D','E','F']]
    for i, p in enumerate(passengers):
        if not p.get('seat_number'):
            p['seat_number'] = seats[i] if i < len(seats) else None
        seating.append(p)
    roster = {
        'flight': {'flight_number': flight.flight_number},
        'pilots': sel_pilots,
        'attendants': sel_att,
        'passengers': seating
    }
    r = Roster(flight_number=flight.flight_number, created_at=datetime.utcnow(), roster_snapshot=roster)
    db.add(r); db.commit(); db.refresh(r)
    return {'roster_id': r.id, 'roster': roster}

@router.get('/{roster_id}/export')
def export(roster_id: int, db: Session = Depends(get_db)):
    r = db.query(Roster).filter(Roster.id==roster_id).first()
    if not r:
        raise HTTPException(404, 'roster not found')
    return r.roster_snapshot


def _save_roster_by_store(session, roster_obj):
    store = os.getenv('ROSTER_STORE','sql')
    if store == 'mongo':
        mongo_uri = os.getenv('MONGO_URI','mongodb://localhost:27017')
        return storage_adapter.save_roster_mongo(mongo_uri, roster_obj)
    else:
        return storage_adapter.save_roster_sql(session, roster_obj)
