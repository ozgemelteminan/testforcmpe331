from typing import List, Dict
from collections import defaultdict
def assign_seats(passengers: List[Dict], seat_map: Dict) -> List[Dict]:
    seats = {s['seat_id']: s for s in seat_map['seats']}
    for p in passengers:
        if p.get('seat_number'):
            sid = p['seat_number']
            if sid in seats:
                seats[sid]['occupied'] = True
    seats_by_row = defaultdict(list)
    for s in seat_map['seats']:
        seats_by_row[s['row']].append(s['seat_id'])
    def find_block(row, needed, seat_type):
        available = [sid for sid in seats_by_row[row] if not seats[sid]['occupied'] and seats[sid]['type']==seat_type]
        if len(available) >= needed:
            return available[:needed]
        return None
    handled = set()
    id_map = {p['id']: p for p in passengers}
    for p in passengers:
        if p['id'] in handled:
            continue
        group_ids = [p['id']]
        if p.get('affiliated'):
            group_ids = [p['id']] + [aid for aid in p['affiliated'] if aid in id_map]
        group = [id_map[g] for g in group_ids]
        seat_type = group[0].get('seat_type', 'economy')
        placed = False
        for row in sorted(seats_by_row.keys()):
            block = find_block(row, len(group), seat_type)
            if block:
                for gi, g in enumerate(group):
                    g['seat_number'] = block[gi]
                    seats[block[gi]]['occupied'] = True
                    handled.add(g['id'])
                placed = True
                break
    free_by_type = {'business': [], 'economy': []}
    for s in seat_map['seats']:
        if not seats[s['seat_id']]['occupied']:
            free_by_type[s['type']].append(s['seat_id'])
    for p in passengers:
        if p.get('seat_number'): continue
        pool = free_by_type.get(p.get('seat_type','economy')) or free_by_type['economy']
        if not pool:
            raise Exception("no available seats for passenger id {}".format(p['id']))
        seat = pool.pop(0)
        p['seat_number'] = seat
        seats[seat]['occupied'] = True
    return passengers
def select_pilots(pool: List[Dict], vehicle: str, distance: int) -> List[Dict]:
    seniors = [p for p in pool if p.get('seniority') == 'senior' and (not p.get('vehicle_restriction') or vehicle in (p.get('vehicle_restriction') if isinstance(p.get('vehicle_restriction'), list) else [p.get('vehicle_restriction')])) and p.get('allowed_range_km',0) >= distance]
    juniors = [p for p in pool if p.get('seniority') == 'junior' and (not p.get('vehicle_restriction') or vehicle in (p.get('vehicle_restriction') if isinstance(p.get('vehicle_restriction'), list) else [p.get('vehicle_restriction')])) and p.get('allowed_range_km',0) >= distance]
    trainees = [p for p in pool if p.get('seniority') == 'trainee' and (not p.get('vehicle_restriction') or vehicle in (p.get('vehicle_restriction') if isinstance(p.get('vehicle_restriction'), list) else [p.get('vehicle_restriction')])) and p.get('allowed_range_km',0) >= distance]
    sel = []
    if seniors:
        sel.append(seniors.pop(0))
    if juniors:
        sel.append(juniors.pop(0))
    candidates = seniors + juniors
    for c in candidates:
        if len(sel) >= 3: break
        sel.append(c)
    tcount = 0
    for t in trainees:
        if len(sel) >= 3: break
        if tcount >= 2: break
        sel.append(t); tcount += 1
    return sel
