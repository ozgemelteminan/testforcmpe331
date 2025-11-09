from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

# ... (Mevcut LocationDetail, FlightBase, FlightCreate, FlightOut kodları burada) ...
class LocationDetail(BaseModel):
    country: Optional[str] = None
    city: Optional[str] = None
    airport_name: Optional[str] = None
    airport_code: str = Field(..., pattern=r"^[A-Z]{3}$", description="3-letter IATA airport code")

class FlightBase(BaseModel):
    flight_number: str = Field(..., pattern=r"^[A-Z]{2}\d{4}$", description="Flight number in AANNNN format")
    departure: Optional[LocationDetail] = None
    arrival: Optional[LocationDetail] = None
    datetime: Optional[str]
    duration_minutes: Optional[int]
    distance: Optional[int]
    vehicle_type: Optional[str]
    shared_with: Optional[Dict[str,Any]] = {}
    menu: Optional[List[str]] = []
    max_passengers: Optional[int] = None
    max_crew: Optional[int] = None
    extra: Optional[Dict[str,Any]] = {}

class FlightCreate(FlightBase):
    pass

class FlightOut(FlightBase):
    id: int
    class Config:
        orm_mode = True

# --- YENİ EKLENDİ: Airport Şemaları ---
class AirportBase(BaseModel):
    name: str
    city: str
    country: str
    iata_code: str = Field(..., pattern=r"^[A-Z]{3}$")

class AirportCreate(AirportBase):
    pass
    
class AirportOut(AirportBase):
    id: int
    class Config:
        orm_mode = True

# --- YENİ EKLENDİ: VehicleType Şemaları ---
class VehicleTypeBase(BaseModel):
    name: str
    seat_map_json: Optional[Dict[str, Any]] = None
    max_passengers_default: Optional[int] = None
    max_crew_default: Optional[int] = None

class VehicleTypeCreate(VehicleTypeBase):
    pass

class VehicleTypeOut(VehicleTypeBase):
    id: int
    class Config:
        orm_mode = True
