CMPE331 - Fixed Project (SQL + NoSQL + Auth)
This fixed project implements:
- SQL storage for Pilot, Cabin, Passenger, Flight services using SQLAlchemy (sqlite examples).
- MongoDB (pymongo) option for saving generated rosters.
- Main system roster generator using utils/roster_utils.py functions.
- JWT auth provider and get_current_user dependency used by all services.

How to run (dev):
- Install requirements: pip install -r requirements.txt
- Start services (examples):
  uvicorn services.pilot_service.app:app --reload --port 8001
  uvicorn services.cabin_service.app:app --reload --port 8002
  uvicorn services.passenger_service.app:app --reload --port 8003
  uvicorn services.flight_info_service.app:app --reload --port 8004
  uvicorn services.main_system.app:app --reload --port 8000
- For MongoDB roster saving, run a local MongoDB instance and update MONGO_URI in utils/storage_adapter.py or env var.

NOTE: This repository is a fixed, minimal full-stack backend to satisfy CMPE331 project specifications.
