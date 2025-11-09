from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class InfantInfo(BaseModel):
    age_months: int
    with_parent_id: Optional[int]

class PassengerBase(BaseModel):
    flight_id: Optional[str] = None  

    name: str
    age: Optional[int]
    gender: Optional[str]
    nationality: Optional[str]
    seat_type: Optional[str]
    seat_number: Optional[str]
    affiliated_ids: Optional[List[int]] = []
    infant: Optional[InfantInfo] = None
    extra: Optional[Dict[str, Any]] = {}

class PassengerCreate(PassengerBase):
    pass

class PassengerOut(PassengerBase):
    id: int

    class Config:
        from_attributes = True
