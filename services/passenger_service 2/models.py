from sqlalchemy import Column, Integer, String, JSON
from .database import Base

class Passenger(Base):
    __tablename__ = "passengers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    nationality = Column(String)
    seat_type = Column(String)  # business / economy
    seat_number = Column(String, nullable=True)
    affiliated_ids = Column(JSON)
    infant = Column(JSON)  # e.g., {'age_months': 10, 'with_parent_id': 5}
    extra = Column(JSON)
