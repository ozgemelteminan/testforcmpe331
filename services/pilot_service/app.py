from fastapi import FastAPI
from .database import engine, Base
from . import models
from .routers import router as pilot_router
Base.metadata.create_all(bind=engine)
app = FastAPI(title='pilot_service')
app.include_router(pilot_router, prefix='/pilots', tags=['pilots'])
