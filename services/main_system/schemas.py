from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class RosterCreate(BaseModel):
    flight_id: str
    flight: Dict[str,Any]
    candidate_pilots: List[Dict[str,Any]]
    candidate_cabin: List[Dict[str,Any]]
    passengers: List[Dict[str,Any]]
    seat_map: List[str]
    requested_by: Optional[str] = None

class RosterOut(BaseModel):
    id: int
    flight_id: str
    data: Dict[str,Any]
