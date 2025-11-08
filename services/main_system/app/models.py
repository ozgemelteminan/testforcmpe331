
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from datetime import datetime

Base = declarative_base()

class Flight(Base):
    __tablename__ = "flights"
    flight_number = Column(String(10), primary_key=True, index=True)
    datetime = Column(DateTime, default=datetime.utcnow)
    distance_km = Column(Integer, default=0)
    vehicle = Column(String(50), default="A320")

class Roster(Base):
    __tablename__ = "rosters"
    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String(10))
    created_at = Column(DateTime)
    roster_snapshot = Column(JSON)
