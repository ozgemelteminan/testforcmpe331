
from fastapi import FastAPI\nfrom utils.postgres_adapter import get_engine, get_session, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from . import models
from .routers import flights, rosters, users
from pathlib import Path

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flight Roster - Main System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(flights.router, prefix="/flights", tags=["flights"])
app.include_router(rosters.router, prefix="/rosters", tags=["rosters"])

@app.get("/")
def root():
    return {"msg": "Flight Roster Main System"}
