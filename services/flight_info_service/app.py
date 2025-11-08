from fastapi import FastAPI
from .database import engine, Base
from .routers import router as flight_router
from . import models
Base.metadata.create_all(bind=engine)
app = FastAPI(title='flight_info_service')
app.include_router(flight_router, prefix='/flights', tags=['flights'])
