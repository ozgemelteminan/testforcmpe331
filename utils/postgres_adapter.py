from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://ozge:mysecret@localhost:5432/flight_roster_db")
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_engine():
    return engine
def get_session():
    return SessionLocal()
