from sqlalchemy import Column, Integer, String, JSON
from .database import Base

class Flight(Base):
    __tablename__ = "flights"
    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, unique=True, index=True)
    
    departure = Column(JSON)
    arrival = Column(JSON)
    
    datetime = Column(String)
    duration_minutes = Column(Integer)
    distance = Column(Integer)
    vehicle_type = Column(String) # DİKKAT: Bu alan artık VehicleType tablosuna 'foreign key' olabilir
    shared_with = Column(JSON)
    menu = Column(JSON)
    
    max_passengers = Column(Integer, nullable=True)
    max_crew = Column(Integer, nullable=True)

    extra = Column(JSON)


# --- YENİ EKLENDİ: Airport (Havalimanı) Modeli ---
# (Arkadaşınızın GET /api/v1/airports/  endpoint'i için)
class Airport(Base):
    __tablename__ = "airports"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    city = Column(String)
    country = Column(String)
    iata_code = Column(String(3), unique=True, index=True) # örn: "IST"

# --- YENİ EKLENDİ: VehicleType (Uçak Tipi) Modeli ---
# (Arkadaşınızın GET /api/v1/vehicle-types/  endpoint'i için)
class VehicleType(Base):
    __tablename__ = "vehicle_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True) # örn: "A320"
    seat_map_json = Column(JSON) # Koltuk planı
    max_passengers_default = Column(Integer)
    max_crew_default = Column(Integer)
