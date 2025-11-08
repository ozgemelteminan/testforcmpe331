Flight Roster — Postgres-fixed package
Generated automatically by assistant.

What I changed / added:
- utils/postgres_adapter.py : SQLAlchemy engine + SessionLocal using DATABASE_URL env var.
- utils/seat_map.py : VEHICLES templates and generate_seat_map_for(vehicle_type).
- utils/roster_utils.py : assign_seats(passengers, seat_map) and select_pilots(pool, vehicle, distance).
- Modified main_system's main.py (if detected) to import postgres_adapter and call Base.metadata.create_all at startup.
- Modified routers/rosters.py (if detected) to include _apply_utils_assignments helper that:
    * generates seat_map from vehicle_type if missing
    * assigns seats to passengers using greedy algorithm (keeps existing assignments)
    * selects pilots from pilot_pool using seniority/vehicle/range rules
- Added docker-compose.postgres.yml to run a Postgres 16 instance for local testing.
- Did NOT modify external service code unless a rosters.py/main.py file was present and modified.

Important notes:
- This environment cannot run or test the services or connect to external DBs.
- After extracting the zip, run:
    pip install -r requirements.txt
    # or ensure psycopg2-binary and sqlalchemy are installed
- Start Postgres:
    docker compose -f docker-compose.postgres.yml up -d
- Set DATABASE_URL environment variable if you want a non-default:
    export DATABASE_URL="postgresql+psycopg2://ozge:mysecret@localhost:5432/flight_roster_db"
- Start main_system service (example):
    uvicorn services.main_system.app.main:app --reload --port 8000

Limitations / what I could not test here:
- I could not run the app or perform database migrations in this environment.
- If project uses custom paths or different import mechanisms, you might need to tweak imports.
- Some services may have their own local DB configs; I added a global utils/postgres_adapter.py to be used by services.

Files modified: 2
Files added: 4 (utils files + docker-compose + README)
