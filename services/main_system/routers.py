# Gerekli import'lar eklendi
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session # EKLENDİ
import random # EKLENDİ

from .schemas import RosterCreate, RosterOut
from services.main_system.database import SessionLocal
from services.main_system.models import Roster # EKLENDİ: Modeli import et
from utils import roster_utils as ru
from utils.storage_adapter import save_roster_by_store
from services.auth.deps import get_current_user

router = APIRouter()

# DÜZELTİLDİ: generate_roster fonksiyonu
@router.post('/generate', response_model=RosterOut, dependencies=[Depends(get_current_user)])
def generate_roster(payload: RosterCreate, store: str = Query('sql', description='sql or mongo')):
    
    flight_data = payload.flight
    
    # --- EKSİK 5: Manuel Mürettebat Seçimi Mantığı EKLENDİ ---
    if payload.manual_pilots:
        pilots = payload.manual_pilots
        # Not: Burada manuel seçimin kurallara uyup uymadığını da kontrol edebilirsiniz
        # Şimdilik, manuel seçimin kuralları ezdiği varsayılmıştır.
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

    # --- EKSİK 4: Araç Kapasite Kontrolü EKLENDİ ---
    max_pax = flight_data.get('max_passengers')
    max_crew_val = flight_data.get('max_crew')
    total_crew = len(pilots) + len(attendants)
    
    # Koltuk ataması
    grouped = ru.group_affiliated_passengers(payload.passengers)
    assigned = ru.assign_affiliated_passengers(grouped, payload.seat_map)
    
    # Bebekler hariç yolcu sayısı (dökümana göre bebeklerin koltuğu yok)
    total_pax = len([p for p in assigned if not p.get('infant')])

    if max_pax is not None and total_pax > max_pax:
        raise HTTPException(status_code=400, detail=f"Passenger count ({total_pax}) exceeds vehicle limit ({max_pax})")
    if max_crew_val is not None and total_crew > max_crew_val:
        raise HTTPException(status_code=400, detail=f"Crew count ({total_crew}) exceeds vehicle limit ({max_crew_val})")

    # Roster objesini oluştur
    roster = {
        'flight_id': payload.flight_id,
        'flight': flight_data, # Düzeltildi: Uçuş bilgisi de eklendi
        'pilots': pilots,
        'attendants': attendants,
        'passengers': assigned,
        'created_by': payload.requested_by
    }

    # --- EKSİK 3: Aşçı Menü Ekleme Mantığı EKLENDİ ---
    chefs_with_recipes = [
        a for a in attendants
        if a.get('attendant_type') == 'chef' and a.get('chef_recipes')
    ]
    if chefs_with_recipes:
        # Uçuşta en az bir aşçı ve tarifi varsa
        selected_chef = random.choice(chefs_with_recipes)
        selected_recipe = random.choice(selected_chef['chef_recipes'])
        
        # Uçuşun menüsüne ekle
        if 'menu' not in roster['flight']:
            roster['flight']['menu'] = []
        roster['flight']['menu'].append(f"Chef's Special: {selected_recipe}")

    # Save
    saved = save_roster_by_store(SessionLocal, roster, store=store)
    
    # Return normalized output for response_model
    if store == 'sql':
        return {'id': saved['id'], 'flight_id': saved['flight_id'], 'data': saved['data']}
    else:
        # Mongo kaydı için ID'yi string'e çevir (RosterOut modeline uyması için)
        # Not: Mongo ID'si SQL ID'si ile karışmasın diye -1 veya str(id) dönebilirsiniz
        # Dökümandaki "view/retrieve" SQL ID'si üzerinden varsayılmıştır.
        mongo_id_str = str(saved.get('_id', -1))
        # RosterOut modeline uyması için 'id' alanını SQL ID gibi -1 yapalım
        return {'id': -1, 'flight_id': saved.get('flight_id'), 'data': saved}


# --- EKSİK 1: "Retrieve" (Geri Getirme) Endpoint'i EKLENDİ ---
@router.get("/{roster_id}", response_model=RosterOut, dependencies=[Depends(get_current_user)])
def retrieve_roster(roster_id: int):
    """
    Retrieve a stored roster by its SQL Database ID.
    This endpoint does not query MongoDB.
    """
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


# --- EKSİK 2: "Export" (Dışa Aktarma) Endpoint'i EKLENDİ ---
@router.get("/{roster_id}/export", dependencies=[Depends(get_current_user)])
def export_roster_json(roster_id: int):
    """
    Export a stored roster's raw JSON data by its SQL Database ID.
    """
    db = SessionLocal()
    try:
        roster_model = db.query(Roster).filter(Roster.id == roster_id).first()
        if not roster_model:
            raise HTTPException(status_code=404, detail="Roster not found in SQL database")
        
        # Dökümanda istendiği gibi sadece JSON verisini döndür
        return roster_model.data
    finally:
        db.close()
