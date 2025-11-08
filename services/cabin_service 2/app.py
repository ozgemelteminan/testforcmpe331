from fastapi import FastAPI
from .database import engine, Base
from . import models
from .routers import router as cabin_router
Base.metadata.create_all(bind=engine)
app = FastAPI(title='cabin_service')
app.include_router(cabin_router, prefix='/attendants', tags=['attendants'])
