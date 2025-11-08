from typing import Any, Dict
import datetime
import os
from sqlalchemy.orm import Session
from pymongo import MongoClient
import json

# SQL roster model will be defined in services.main_system.models
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
MONGO_DB = os.environ.get('MONGO_DB', 'cmpe331')

def save_roster_by_store(db_or_session: Any, roster: Dict, store: str = "sql"):
    roster = dict(roster)
    roster['created_at'] = datetime.datetime.utcnow().isoformat()
    if store == "sql":
        # db_or_session is SQLAlchemy Session
        SessionLocal = db_or_session
        # import lazily to avoid circular imports
        from services.main_system.models import Roster as RosterModel
        db = SessionLocal()
        r = RosterModel(flight_id=roster.get('flight_id'), data=roster)
        db.add(r)
        db.commit()
        db.refresh(r)
        db.close()
        return {"id": r.id, "flight_id": r.flight_id, "data": roster}
    elif store == "mongo":
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        coll = db['rosters']
        res = coll.insert_one(roster)
        roster['_id'] = str(res.inserted_id)
        client.close()
        return roster
    else:
        raise ValueError("Unsupported store type: %s" % store)
