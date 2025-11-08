
# Flight Roster - Minimal Demo Project

Bu repo FastAPI ile hazırlanmış örnek bir flight-roster sistemidir. Swagger/OpenAPI dokümantasyonu otomatik olarak FastAPI tarafından sağlanır (`/docs`).

## İçerik
- main_system: SQLAlchemy ile basit bir ana uygulama (roster oluşturma, flights, rosters)
- flight_info_service, pilot_service, cabin_service, passenger_service: küçük demo FastAPI servisleri (in-memory)

## Çalıştırma (lokal geliştirici modu)
1. Python 3.10+ virtualenv oluşturun ve aktif edin.
2. `pip install -r requirements.txt`
3. Her servisi ayrı terminalde çalıştırın:
   - `uvicorn services.flight_info_service.app:app --port 8001 --reload`
   - `uvicorn services.pilot_service.app:app --port 8002 --reload`
   - `uvicorn services.cabin_service.app:app --port 8003 --reload`
   - `uvicorn services.passenger_service.app:app --port 8004 --reload`
   - `uvicorn services.main_system.app.main:app --port 8000 --reload`

4. Swagger UI'ya gidin: `http://localhost:8000/docs` (main system) ve diğer servislerin `/docs` adresleri.

## Notlar
- Main system varsayılan olarak `DATABASE_URL` environment variable'ını kullanır. Local MySQL yoksa SQL kısmı hata verebilir; demo amaçlı in-memory ve servisler ile çalışmak için kod basitleştirilmiştir.
- Zip içindeki dosyalar doğrudan düzenlenip çalıştırılabilir.

