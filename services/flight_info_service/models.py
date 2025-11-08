from sqlalchemy import Column, Integer, String, JSON
from .database import Base
class Flight(Base):
    __tablename__ = "flights"
    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, unique=True, index=True)
    departure = Column(String)
    arrival = Column(String)
    datetime = Column(String)
    duration_minutes = Column(Integer)
    distance = Column(Integer)
    vehicle_type = Column(String)
    shared_with = Column(JSON)
    menu = Column(JSON)
    extra = Column(JSON)
