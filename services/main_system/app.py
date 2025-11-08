from fastapi import FastAPI
from .database import engine, Base
from .routers import router as rosters_router
Base.metadata.create_all(bind=engine)
app = FastAPI(title='main_system')
app.include_router(rosters_router, prefix='/rosters', tags=['rosters'])
