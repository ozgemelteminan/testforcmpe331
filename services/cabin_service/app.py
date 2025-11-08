
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
app = FastAPI(title="Cabin Service")

class Attendant(BaseModel):
    id: str
    name: str
    attendant_type: str = "regular"  # chief, regular, chef
    vehicle_restrictions: List[str] = []

DB = []

@app.post("/attendants", status_code=201)
def add(a: Attendant):
    DB.append(a.dict())
    return {"ok": True}

@app.get("/attendants", response_model=List[Attendant])
def list_attendants():
    return DB
