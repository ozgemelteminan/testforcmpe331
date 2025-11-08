from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class PilotBase(BaseModel):
    name: str
    age: Optional[int]
    gender: Optional[str]
    nationality: Optional[str]
    known_languages: Optional[List[str]] = []
    vehicle_restriction: Optional[List[str]] = []
    allowed_range: Optional[int]
    seniority: Optional[str]
    extra: Optional[Dict[str,Any]] = {}

class PilotCreate(PilotBase):
    pass
class PilotOut(PilotBase):
    id: int
    class Config:
        orm_mode = True
