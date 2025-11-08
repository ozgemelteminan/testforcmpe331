from sqlalchemy import Column, Integer, String, JSON
from .database import Base

class Flight(Base):
    __tablename__ = "flights"
    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, unique=True, index=True)
    
    # DÜZELTİLDİ: (Eksik 6) String yerine JSON (yapısal veriyi saklamak için)
    departure = Column(JSON)
    arrival = Column(JSON)
    
    datetime = Column(String)
    duration_minutes = Column(Integer)
    distance = Column(Integer)
    vehicle_type = Column(String)
    shared_with = Column(JSON)
    menu = Column(JSON)
    
    # EKLENDİ: (Eksik 4) Uçak kapasite limitleri
    max_passengers = Column(Integer, nullable=True)
    max_crew = Column(Integer, nullable=True)

    extra = Column(JSON)
