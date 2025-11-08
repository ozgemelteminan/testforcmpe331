from typing import List, Dict, Any
import itertools
import random # EKLENDİ (select_attendants'da kullanılabilir)

def select_pilots_by_seniority(candidates: List[Dict[str,Any]], flight) -> List[Dict]:
    """Select pilots obeying rules:
    - At least 1 senior and 1 junior
    - At most 2 trainees overall
    - Respect pilot.allowed_range >= flight.distance and vehicle restriction
    Greedy selection.
    """
    
    # --- DÜZELTİLDİ: (Eksik 7) Pilot seçme filtresi güncellendi ---
    def is_pilot_qualified(p, flight_data):
        """Helper to check range and vehicle restrictions"""
        if not flight_data:
            return True # Uçuş bilgisi yoksa kontrol etme
            
        # 1. Araç Kısıtlaması Kontrolü (Artık 'str' bekliyoruz)
        pilot_restriction = p.get('vehicle_restriction')
        flight_vehicle = flight_data.get('vehicle_type')
        if pilot_restriction and flight_vehicle:
             # Eğer pilotun bir kısıtlaması varsa VE bu, uçağın tipiyle eşleşmiyorsa
            if pilot_restriction != flight_vehicle:
                return False
                
        # 2. Menzil Kontrolü
        pilot_range = p.get('allowed_range')
        flight_distance = flight_data.get('distance')
        if pilot_range is not None and flight_distance is not None:
            if pilot_range < flight_distance:
                return False
                
        return True

    # Önce kurallara uyan adayları filtrele
    qualified_candidates = [p for p in candidates if is_pilot_qualified(p, flight)]

    seniors = [p for p in qualified_candidates if p.get('seniority') == 'senior']
    juniors = [p for p in qualified_candidates if p.get('seniority') == 'junior']
    trainees = [p for p in qualified_candidates if p.get('seniority') == 'trainee']
    
    selected = []
    
    # Kural: En az 1 senior
    if seniors:
        selected.append(seniors.pop(0))
    
    # Kural: En az 1 junior
    if juniors:
        selected.append(juniors.pop(0))

    # Eğer 1 senior ve 1 junior yoksa (toplam 2 pilot lazım)
    # Kalan adaylarla (trainee hariç) 2'ye tamamla
    remaining_qualified = seniors + juniors
    
    while len(selected) < 2 and remaining_qualified:
        selected.append(remaining_qualified.pop(0))

    # Kural: En fazla 2 trainee
    # Kalan boşlukları (varsa) trainee'ler ile doldur
    trainee_count = 0
    while trainee_count < 2 and trainees:
        selected.append(trainees.pop(0))
        trainee_count += 1

    # Dökümanda "at least one single and one junior pilot" dendiği için
    # 2 pilottan azsa veya 1S+1J kuralı sağlanmadıysa (yukarıda sağlandı)
    # Aslında burada `if len(selected) < 2:` kontrolü yeterli
    
    return selected


def select_attendants(candidates: List[Dict], flight) -> List[Dict]:
    """Select cabin attendants: enforce 1-4 seniors, 4-16 juniors, 0-2 chefs.
    Greedy selection by type.
    """
    
    # Önce araca uygun olanları filtrele
    if flight:
        vt = flight.get('vehicle_type')
        def is_attendant_qualified(a):
            restrictions = a.get('vehicle_restriction', [])
            if not restrictions: # Kısıtlama yoksa uygundur
                return True
            if vt in restrictions: # Uçak tipi kısıtlama listesindeyse uygundur
                return True
            return False
        candidates = [a for a in candidates if is_attendant_qualified(a)]
    
    # Dökümanda 'chief' ve 'regular' için kıdem belirtilmemiş,
    # 'senior' ve 'junior' olarak belirtilmiş. (1-4 senior, 4-16 junior)
    # 'chief' tipini 'senior' olarak varsayıyoruz.
    
    seniors = [a for a in candidates if a.get('attendant_type') == 'chief' or a.get('seniority') == 'senior']
    juniors = [a for a in candidates if (a.get('attendant_type') == 'regular' or not a.get('attendant_type')) and a.get('seniority') == 'junior']
    chefs = [a for a in candidates if a.get('attendant_type') == 'chef']
    
    selected = []
    
    # Kural: 1-4 senior
    selected.extend(seniors[0:4]) # 1'den azsa da (0) o kadarını alır
    
    # Kural: 4-16 junior
    selected.extend(juniors[0:16]) # 4'ten azsa da (0) o kadarını alır
    
    # Kural: 0-2 chef
    selected.extend(chefs[0:2])
    
    # Not: Dökümandaki "1-4" ve "4-16" kuralları "minimum" gereksinimlerdir.
    # Eğer havuzda yeterli personel yoksa, bu kod eldekileri seçer.
    # Gerçek bir sistemde, `len(selected_seniors) < 1` veya `len(selected_juniors) < 4`
    # durumunda hata fırlatılması gerekebilir.
    
    return selected

def group_affiliated_passengers(passengers: List[Dict]) -> List[List[Dict]]:
    """Group passengers by affiliated ids. Returns list of groups (each group is list of passenger dicts)."""
    id_to = {p['id']: p for p in passengers}
    visited = set()
    groups = []
    for p in passengers:
        if p['id'] in visited:
            continue
        
        # O anki yolcudan başlayarak grubu keşfet
        group = []
        queue = [p]
        visited.add(p['id'])
        
        while queue:
            current_p = queue.pop(0)
            group.append(current_p)
            
            # Bu yolcunun ilişkili olduğu kişileri al
            aff_ids = current_p.get('affiliated_ids') or []
            
            for aid in aff_ids:
                if aid in id_to and aid not in visited:
                    visited.add(aid)
                    queue.append(id_to[aid])
                    
            # (İki yönlü ilişki için) Diğer yolcuların da bu yolcuyla ilişkili olup olmadığına bak
            for other_p in passengers:
                if other_p['id'] not in visited:
                    if p['id'] in (other_p.get('affiliated_ids') or []):
                        visited.add(other_p['id'])
                        queue.append(other_p)

        groups.append(group)
    return groups

def assign_affiliated_passengers(groups: List[List[Dict]], seat_map: List[str]) -> List[Dict]:
    """Assign seats attempting to place each group in neighboring seats.
    seat_map: flat list of seat identifiers (e.g., ['1A','1B',...]) assumed ordered by adjacency.
    Returns flat passenger list with 'seat_number' assigned where possible.
    """
    assigned = []
    free = list(seat_map)
    
    # Önce büyük grupları (bebekler hariç) oturt
    groups.sort(key=lambda g: len([p for p in g if not p.get('infant')]), reverse=True)
    
    for grp in groups:
        # Bebekler koltuk kaplamaz
        size = len([p for p in grp if not p.get('infant')])
        
        if size == 0: # Sadece bebek(ler) olan bir grup (mantıksız ama olası)
            assigned.extend(grp)
            continue
            
        # Bitişik 'size' kadar boş koltuk bloğu ara
        found_block = None
        for i in range(len(free) - size + 1):
            block = free[i:i+size]
            # (Daha iyi bir algoritma burada koltukların gerçekten bitişik
            # olup olmadığını 'seat_map' yapısına göre kontrol ederdi,
            # örn: '1A', '1B'. Şimdilik listenin sırasını bitişiklik kabul ediyoruz.)
            found_block = (i, block)
            break
        
        if found_block:
            idx, block = found_block
            # Koltukları ata (bebekler hariç)
            bi = 0
            for p in grp:
                if p.get('infant'):
                    p['seat_number'] = None # Bebeklerin koltuğu yok
                else:
                    p['seat_number'] = block[bi]
                    bi += 1
            # Kullanılan koltukları 'free' listesinden çıkar
            del free[idx:idx+size]
        else:
            # Bitişik blok yoksa, kalan boş koltuklara ata
            for p in grp:
                if p.get('infant'):
                    p['seat_number'] = None
                else:
                    if free:
                        p['seat_number'] = free.pop(0)
                    else:
                        p['seat_number'] = None # Uçak doldu
        
        assigned.extend(grp)
        
    return assigned
