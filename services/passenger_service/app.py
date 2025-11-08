from fastapi import FastAPI
from .database import engine, Base
from .routers import router as passenger_router
from . import models
Base.metadata.create_all(bind=engine)
app = FastAPI(title='passenger_service')
app.include_router(passenger_router, prefix='/passengers', tags=['passengers'])
