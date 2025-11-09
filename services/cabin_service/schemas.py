from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class AttendantBase(BaseModel):
    name: str
    age: Optional[int]
    gender: Optional[str]
    nationality: Optional[str]
    known_languages: Optional[List[str]] = []
    attendant_type: Optional[str]
    chef_recipes: Optional[List[str]] = []
    vehicle_restriction: Optional[List[str]] = []
    seniority: Optional[str]
    extra: Optional[Dict[str,Any]] = {}

class AttendantCreate(AttendantBase):
    pass
class AttendantOut(AttendantBase):
    id: int
    class Config:
        from_attributes = True
