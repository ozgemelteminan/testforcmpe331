from sqlalchemy import Column, Integer, String, JSON
from .database import Base

class Pilot(Base):
    __tablename__ = "pilots"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)
    nationality = Column(String)
    known_languages = Column(JSON)
    
    # DÜZELTİLDİ: (Eksik 7) JSON (liste) yerine String (tekil)
    vehicle_restriction = Column(String, nullable=True) # JSON idi
    
    allowed_range = Column(Integer)
    seniority = Column(String)
    extra = Column(JSON)
