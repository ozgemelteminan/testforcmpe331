
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
app = FastAPI(title="Pilot Service")

class Pilot(BaseModel):
    id: str
    name: str
    seniority: str = "junior"
    vehicle_restriction: str = ""
    allowed_range_km: int = 2000

DB = []

@app.post("/pilots", status_code=201)
def add(p: Pilot):
    DB.append(p.dict())
    return {"ok": True}

@app.get("/pilots", response_model=List[Pilot])
def list_pilots():
    return DB
