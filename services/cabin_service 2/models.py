from sqlalchemy import Column, Integer, String, JSON
from .database import Base

class Attendant(Base):
    __tablename__ = "attendants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    nationality = Column(String)
    known_languages = Column(JSON)
    attendant_type = Column(String)  # chief / regular / chef
    chef_recipes = Column(JSON)
    vehicle_restriction = Column(JSON)
    seniority = Column(String)
    extra = Column(JSON)
