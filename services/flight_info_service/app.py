
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
app = FastAPI(title="Flight Info Service")

class Flight(BaseModel):
    flight_number: str
    datetime: datetime
    duration_mins: int = 0
    distance_km: int = 0
    src_code: str = ""
    dst_code: str = ""
    vehicle_type: str = ""

DB = {}

@app.post("/flights", status_code=201)
def add(f: Flight):
    if f.flight_number in DB:
        raise HTTPException(400, "flight exists")
    DB[f.flight_number] = f.dict()
    return {"ok": True, "flight": DB[f.flight_number]}

@app.get("/flights")
def list_flights():
    return list(DB.values())

@app.get("/flights/{flight_number}")
def get_flight(flight_number: str):
    if flight_number not in DB:
        raise HTTPException(404, "notfound")
    return DB[flight_number]
