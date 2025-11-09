from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class PilotBase(BaseModel):
    name: str
    age: Optional[int]
    gender: Optional[str]
    nationality: Optional[str]
    known_languages: Optional[List[str]] = []
    
    # DÜZELTİLDİ: (Eksik 7) Dökümana göre "single" (tekil) olmalı
    vehicle_restriction: Optional[str] = None # List[str] idi
    
    allowed_range: Optional[int]
    seniority: Optional[str]
    extra: Optional[Dict[str,Any]] = {}

class PilotCreate(PilotBase):
    pass
class PilotOut(PilotBase):
    id: int
    class Config:
        from_attributes = True
