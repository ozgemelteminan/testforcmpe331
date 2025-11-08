from pydantic import BaseModel
from typing import Optional, List, Dict, Any
class FlightBase(BaseModel):
    flight_number: str
    departure: Optional[str]
    arrival: Optional[str]
    datetime: Optional[str]
    duration_minutes: Optional[int]
    distance: Optional[int]
    vehicle_type: Optional[str]
    shared_with: Optional[Dict[str,Any]] = {}
    menu: Optional[List[str]] = []
    extra: Optional[Dict[str,Any]] = {}
class FlightCreate(FlightBase):
    pass
class FlightOut(FlightBase):
    id: int
    class Config:
        orm_mode = True
