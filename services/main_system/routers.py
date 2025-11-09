# Gerekli import'lar eklendi
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session # EKLENDİ
import random # EKLENDİ
from typing import List, Dict, Any # EKLENDİ

from .schemas import RosterCreate, RosterOut
from services.main_system.database import SessionLocal
from services.main_system.models import Roster # EKLENDİ: Modeli import et
from utils import roster_utils as ru
from utils.storage_adapter import save_roster_by_store
# DÜZELTME: Admin yetkisi de import edildi (POST için)
from services.auth.deps import get_current_user, get_current_admin_user

router = APIRouter()

# DÜZELTME: generate_roster artık 'admin' yetkisi istiyor
@router.post('/generate', response_model=RosterOut, dependencies=[Depends(get_current_admin_user)])
def generate_roster(payload: RosterCreate, store: str = Query('sql', description='sql or mongo')):
    
    flight_data = payload.flight
    
    # --- Manuel Mürettebat Seçimi Mantığı ---
    if payload.manual_pilots:
        pilots = payload.manual_pilots
    elif payload.candidate_pilots:
        pilots = ru.select_pilots_by_seniority(payload.candidate_pilots, flight_data)
        if len(pilots) < 2:
            raise HTTPException(status_code=400, detail='Not enough pilots selected by rules (Req: 1 Senior, 1 Junior)')
    else:
        raise HTTPException(status_code=400, detail="Must provide one of 'manual_pilots' or 'candidate_pilots'")

    if payload.manual_cabin:
        attendants = payload.manual_cabin
    elif payload.candidate_cabin:
        attendants = ru.select_attendants(payload.candidate_cabin, flight_data)
    else:
        raise HTTPException(status_code=400, detail="Must provide one of 'manual_cabin' or 'candidate_cabin'")

    # --- Araç Kapasite Kontrolü ---
    max_pax = flight_data.get('max_passengers')
    max_crew_val = flight_data.get('max_crew')
    total_crew = len(pilots) + len(attendants)
    
    grouped = ru.group_affiliated_passengers(payload.passengers)
    assigned = ru.assign_affiliated_passengers(grouped, payload.seat_map)
    total_pax = len([p for p in assigned if not p.get('infant')])

    if max_pax is not None and total_pax > max_pax:
        raise HTTPException(status_code=400, detail=f"Passenger count ({total_pax}) exceeds vehicle limit ({max_pax})")
    if max_crew_val is not None and total_crew > max_crew_val:
        raise HTTPException(status_code=400, detail=f"Crew count ({total_crew}) exceeds vehicle limit ({max_crew_val})")

    roster = {
        'flight_id': payload.flight_id,
        'flight': flight_data,
        'pilots': pilots,
        'attendants': attendants,
        'passengers': assigned,
        'created_by': payload.requested_by
    }

    # --- Aşçı Menü Ekleme Mantığı ---
    chefs_with_recipes = [
        a for a in attendants
        if a.get('attendant_type') == 'chef' and a.get('chef_recipes')
    ]
    if chefs_with_recipes:
        selected_chef = random.choice(chefs_with_recipes)
        selected_recipe = random.choice(selected_chef['chef_recipes'])
        if 'menu' not in roster['flight']:
            roster['flight']['menu'] = []
        roster['flight']['menu'].append(f"Chef's Special: {selected_recipe}")

    # Save
    saved = save_roster_by_store(SessionLocal, roster, store=store)
    
    if store == 'sql':
        return {'id': saved['id'], 'flight_id': saved['flight_id'], 'data': saved['data']}
    else:
        return {'id': -1, 'flight_id': saved.get('flight_id'), 'data': saved}


# --- "Retrieve" (Geri Getirme) Endpoint'i ---
@router.get("/{roster_id}", response_model=RosterOut, dependencies=[Depends(get_current_user)])
def retrieve_roster(roster_id: int):
    db = SessionLocal()
    try:
        roster_model = db.query(Roster).filter(Roster.id == roster_id).first()
        if not roster_model:
            raise HTTPException(status_code=404, detail="Roster not found in SQL database")
        
        return RosterOut(
            id=roster_model.id,
            flight_id=roster_model.flight_id,
            data=roster_model.data
        )
    finally:
        db.close()

# --- "Export" (Dışa Aktarma) Endpoint'i ---
@router.get("/{roster_id}/export", dependencies=[Depends(get_current_user)])
def export_roster_json(roster_id: int):
    db = SessionLocal()
    try:
        roster_model = db.query(Roster).filter(Roster.id == roster_id).first()
        if not roster_model:
            raise HTTPException(status_code=404, detail="Roster not found in SQL database")
        
        return roster_model.data
    finally:
        db.close()


# --- YENİ EKLENEN ÖZEL GÖRÜNÜM (VIEW) ENDPOINT'LERİ ---

# Yardımcı fonksiyon (DRY - Don't Repeat Yourself)
def get_roster_data_from_db(roster_id: int, db: Session) -> Dict[str, Any]:
    roster_model = db.query(Roster).filter(Roster.id == roster_id).first()
    if not roster_model:
        raise HTTPException(status_code=404, detail="Roster not found in SQL database")
    if not isinstance(roster_model.data, dict):
         raise HTTPException(status_code=500, detail="Roster data is corrupted")
    return roster_model.data

# 1. Tabular View Endpoint'i
@router.get("/{roster_id}/tabular-view", dependencies=[Depends(get_current_user)])
def get_tabular_view(roster_id: int):
    """
    Provides data formatted for the 'Tabular View' as required by the specifications.
    (Returns a list of all personnel (Pilot, Cabin, Passenger) with their Type, ID, and Name).
    """
    db = SessionLocal()
    try:
        roster_data = get_roster_data_from_db(roster_id, db)
        
        tabular_list = []
        
        # Pilotları ekle
        for p in roster_data.get('pilots', []):
            tabular_list.append({
                "type": "Pilot",
                "id": p.get('id'),
                "name": p.get('name')
            })
            
        # Kabin ekibini ekle
        for a in roster_data.get('attendants', []):
            tabular_list.append({
                "type": "Cabin Crew",
                "id": a.get('id'),
                "name": a.get('name')
            })
            
        # Yolcuları ekle (Bebekler hariç?)
        for px in roster_data.get('passengers', []):
            if not px.get('infant'): # Bebek değilse
                tabular_list.append({
                    "type": "Passenger",
                    "id": px.get('id'),
                    "name": px.get('name')
                })
                
        return tabular_list
    finally:
        db.close()

# 2. Extended View Endpoint'i
@router.get("/{roster_id}/extended-view", dependencies=[Depends(get_current_user)])
def get_extended_view(roster_id: int):
    """
    Provides data for the 'Extended View' as required by the specifications.
    (Returns 3 separate JSON lists for Pilots, Cabin Crew, and Passengers).
    """
    db = SessionLocal()
    try:
        roster_data = get_roster_data_from_db(roster_id, db)
        
        # Veriyi 3 ana başlık altında topla
        extended_data = {
            "pilots": roster_data.get('pilots', []),
            "cabin_crew": roster_data.get('attendants', []),
            "passengers": roster_data.get('passengers', [])
        }
        return extended_data
    finally:
        db.close()

# 3. Plane View Endpoint'i
@router.get("/{roster_id}/plane-view", dependencies=[Depends(get_current_user)])
def get_plane_view(roster_id: int):
    """
    Provides data for the 'Plane View' as required by the specifications.
    (Returns the final list of passengers with their seat assignments).
    """
    db = SessionLocal()
    try:
        roster_data = get_roster_data_from_db(roster_id, db)
        
        # Dökümandaki gibi, bu görünümün amacı atanmış yolcu listesidir.
        # Bu veri zaten 'passengers' anahtarı altında mevcut.
        return {
            "flight": roster_data.get('flight'),
            "assigned_passengers": roster_data.get('passengers', [])
        }
    finally:
        db.close()
