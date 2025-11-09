from pydantic import BaseModel, Field # Field eklendi
from typing import Optional, List, Dict, Any

# EKLENDİ: (Eksik 6) Kaynak/Hedef için yapısal (structured) model
class LocationDetail(BaseModel):
    country: Optional[str] = None
    city: Optional[str] = None
    airport_name: Optional[str] = None
    # EKLENDİ: (Eksik 8) AAA formatı için Regex doğrulaması
    airport_code: str = Field(..., pattern=r"^[A-Z]{3}$", description="3-letter IATA airport code")

class FlightBase(BaseModel):
    # DÜZELTİLDİ: (Eksik 8) AANNNN formatı için Regex doğrulaması
    flight_number: str = Field(..., pattern=r"^[A-Z]{2}\d{4}$", description="Flight number in AANNNN format")
    
    # DÜZELTİLDİ: (Eksik 6) String yerine yapısal model kullan
    departure: Optional[LocationDetail] = None
    arrival: Optional[LocationDetail] = None
    
    datetime: Optional[str]
    duration_minutes: Optional[int]
    distance: Optional[int]
    vehicle_type: Optional[str]
    shared_with: Optional[Dict[str,Any]] = {}
    menu: Optional[List[str]] = []
    
    # EKLENDİ: (Eksik 4) Uçak kapasite limitleri
    max_passengers: Optional[int] = None
    max_crew: Optional[int] = None

    extra: Optional[Dict[str,Any]] = {}

class FlightCreate(FlightBase):
    pass

class FlightOut(FlightBase):
    id: int
    class Config:
        orm_mode = True
