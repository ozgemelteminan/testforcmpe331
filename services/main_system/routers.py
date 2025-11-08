from fastapi import APIRouter, Depends, HTTPException, Query
from .schemas import RosterCreate, RosterOut
from services.main_system.database import SessionLocal
from utils import roster_utils as ru
from utils.storage_adapter import save_roster_by_store
from services.auth.deps import get_current_user

router = APIRouter()

@router.post('/generate', response_model=RosterOut, dependencies=[Depends(get_current_user)])
def generate_roster(payload: RosterCreate, store: str = Query('sql', description='sql or mongo')):
    # 1. Select pilots
    pilots = ru.select_pilots_by_seniority(payload.candidate_pilots, payload.flight)
    if len(pilots) < 2:
        raise HTTPException(status_code=400, detail='Not enough pilots selected by rules')
    attendants = ru.select_attendants(payload.candidate_cabin, payload.flight)
    grouped = ru.group_affiliated_passengers(payload.passengers)
    assigned = ru.assign_affiliated_passengers(grouped, payload.seat_map)
    roster = {
        'flight_id': payload.flight_id,
        'pilots': pilots,
        'attendants': attendants,
        'passengers': assigned,
        'created_by': payload.requested_by
    }
    # Save
    saved = save_roster_by_store(SessionLocal, roster, store=store)
    # Return normalized output for response_model
    if store == 'sql':
        return {'id': saved['id'], 'flight_id': saved['flight_id'], 'data': saved['data']}
    else:
        return {'id': -1, 'flight_id': saved.get('flight_id'), 'data': saved}
