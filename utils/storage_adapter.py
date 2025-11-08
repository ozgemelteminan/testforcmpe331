import os, json
from utils.postgres_adapter import get_engine, get_session
try:
    from pymongo import MongoClient
except Exception:
    MongoClient = None
def save_roster_sql(session, roster_obj):
    from services.main_system.app.models import Roster as RosterModel
    r = RosterModel(flight_number=roster_obj.get('flight', {}).get('flight_number',''), snapshot_json=json.dumps(roster_obj))
    session.add(r); session.commit(); session.refresh(r)
    return r.id
def save_roster_mongo(mongo_uri, roster_obj):
    if MongoClient is None:
        raise RuntimeError("pymongo not installed")
    client = MongoClient(mongo_uri)
    db = client.get_database(os.getenv('MONGO_DB','rosterdb'))
    col = db.get_collection('rosters')
    res = col.insert_one({"flight_number": roster_obj.get('flight', {}).get('flight_number',''), "roster": roster_obj})
    return str(res.inserted_id)
