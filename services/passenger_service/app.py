
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
app = FastAPI(title="Passenger Service")

class Passenger(BaseModel):
    id: str
    flight_number: str
    name: str
    age: int = 30
    seat_type: str = "economy"  # business/economy
    seat_number: Optional[str] = None
    affiliated: List[str] = []

DB = []

@app.post("/passengers", status_code=201)
def add(p: Passenger):
    DB.append(p.dict())
    return {"ok": True}

@app.get("/passengers/by-flight/{flight_number}", response_model=List[Passenger])
def by_flight(flight_number: str):
    return [p for p in DB if p['flight_number'] == flight_number]
