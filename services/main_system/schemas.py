from pydantic import BaseModel, root_validator
from typing import List, Dict, Any, Optional

class RosterCreate(BaseModel):
    flight_id: str
    flight: Dict[str,Any]
    
    # DÜZELTİLDİ: (Eksik 5) Manuel seçime izin ver
    candidate_pilots: Optional[List[Dict[str,Any]]] = None
    candidate_cabin: Optional[List[Dict[str,Any]]] = None
    manual_pilots: Optional[List[Dict[str,Any]]] = None
    manual_cabin: Optional[List[Dict[str,Any]]] = None
    
    passengers: List[Dict[str,Any]]
    seat_map: List[str] # Not: Bu 'seat_map' aslında utils/seat_map.py'den üretilmeli
    requested_by: Optional[str] = None

    # EKLENDİ: (Eksik 5) Doğrulayıcı
    @root_validator(pre=False, skip_on_failure=True)
    def check_crew_selection_method(cls, values):
        # Pilotlar için kontrol
        if not values.get('manual_pilots') and not values.get('candidate_pilots'):
            raise ValueError("Either 'manual_pilots' or 'candidate_pilots' must be provided")
        if values.get('manual_pilots') and values.get('candidate_pilots'):
            raise ValueError("Cannot provide both 'manual_pilots' and 'candidate_pilots'")
        
        # Kabin ekibi için kontrol
        if not values.get('manual_cabin') and not values.get('candidate_cabin'):
            raise ValueError("Either 'manual_cabin' or 'candidate_cabin' must be provided")
        if values.get('manual_cabin') and values.get('candidate_cabin'):
            raise ValueError("Cannot provide both 'manual_cabin' and 'candidate_cabin'")
            
        return values

class RosterOut(BaseModel):
    id: int
    flight_id: str
    data: Dict[str,Any]
