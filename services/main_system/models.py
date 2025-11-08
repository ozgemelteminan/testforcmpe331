from sqlalchemy import Column, Integer, String, JSON
from .database import Base

class Roster(Base):
    __tablename__ = "rosters"
    id = Column(Integer, primary_key=True, index=True)
    flight_id = Column(String, index=True)
    data = Column(JSON)
