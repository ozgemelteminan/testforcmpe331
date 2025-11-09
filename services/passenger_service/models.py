from sqlalchemy import Column, Integer, String, JSON
from .database import Base

class Passenger(Base):
    __tablename__ = "passengers"

    id = Column(Integer, primary_key=True, index=True)
    flight_id = Column(String, nullable=True)  # ✅ eklendi — uçuş numarası

    name = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    nationality = Column(String, nullable=True)
    seat_type = Column(String, nullable=True)
    seat_number = Column(String, nullable=True)

    affiliated_ids = Column(JSON, nullable=True)  # liste şeklinde
    infant = Column(JSON, nullable=True)          # bebek bilgisi
    extra = Column(JSON, nullable=True)           # opsiyonel ek alanlar
