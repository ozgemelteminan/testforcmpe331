from fastapi import FastAPI
from .database import engine, Base
from .routers import router as flight_router
from . import models
                                    # Eğer bölmediysen sadece 'from . import models' yeterli

# DÜZELTME: Tüm modelleri (Flight, Airport, VehicleType) oluştur
Base.metadata.create_all(bind=engine)

app = FastAPI(title='flight_info_service')

# DÜZELTME: Prefix'i (önek) app.include_router'dan alıp
# routers.py dosyasındaki APIRouter() içine taşıdık.
# Bu yüzden buradaki prefix'i kaldırıyoruz.
app.include_router(flight_router, tags=['flight_info'])
