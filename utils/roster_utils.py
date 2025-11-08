from typing import List, Dict, Any
import itertools

def select_pilots_by_seniority(candidates: List[Dict[str,Any]], flight) -> List[Dict]:
    """Select pilots obeying rules:
    - At least 1 senior and 1 junior
    - At most 2 trainees overall
    - Respect pilot.allowed_range >= flight.distance and vehicle restriction
    Greedy selection.
    """
    seniors = [p for p in candidates if p.get('seniority') == 'senior']
    juniors = [p for p in candidates if p.get('seniority') == 'junior']
    trainees = [p for p in candidates if p.get('seniority') == 'trainee']
    selected = []
    # pick one senior, one junior if available
    if seniors:
        selected.append(seniors[0])
    if juniors:
        selected.append(juniors[0])
    # fill additional slots (e.g., second pilot) prefer junior then trainee
    remaining = [p for p in candidates if p not in selected]
    for p in remaining:
        if len([x for x in selected if x.get('seniority')=='trainee']) >= 2:
            # can't add more trainees
            if p.get('seniority') == 'trainee':
                continue
        selected.append(p)
        if len(selected) >= 2:
            break
    # filter by vehicle and allowed_range if flight provided
    if flight:
        def ok(p):
            if 'vehicle_restriction' in p and p['vehicle_restriction']:
                if flight.get('vehicle_type') not in p['vehicle_restriction']:
                    return False
            if p.get('allowed_range') is not None:
                if p['allowed_range'] < flight.get('distance', 0):
                    return False
            return True
        selected = [p for p in selected if ok(p)]
    return selected

def select_attendants(candidates: List[Dict], flight) -> List[Dict]:
    """Select cabin attendants: enforce 1-4 seniors, 4-16 juniors, 0-2 chefs.
    Greedy selection by type.
    """
    chiefs = [a for a in candidates if a.get('attendant_type') == 'chief' or a.get('seniority')=='senior']
    juniors = [a for a in candidates if a.get('seniority') == 'junior' and a.get('attendant_type')!='chef']
    chefs = [a for a in candidates if a.get('attendant_type') == 'chef']
    selected = []
    # take 1-4 seniors (chiefs)
    selected.extend(chiefs[:4])
    # take 4-16 juniors
    need_j = max(4, min(16, len(juniors)))
    selected.extend(juniors[:need_j])
    # take up to 2 chefs
    selected.extend(chefs[:2])
    # filter by vehicle restriction
    if flight:
        vt = flight.get('vehicle_type')
        selected = [a for a in selected if (not a.get('vehicle_restriction')) or vt in a.get('vehicle_restriction',[])]
    return selected

def group_affiliated_passengers(passengers: List[Dict]) -> List[List[Dict]]:
    """Group passengers by affiliated ids. Returns list of groups (each group is list of passenger dicts)."""
    id_to = {p['id']: p for p in passengers}
    visited = set()
    groups = []
    for p in passengers:
        if p['id'] in visited:
            continue
        group = [p]
        visited.add(p['id'])
        aff = p.get('affiliated_ids') or []
        for aid in aff:
            if aid in id_to and aid not in visited:
                group.append(id_to[aid])
                visited.add(aid)
        groups.append(group)
    return groups

def assign_affiliated_passengers(groups: List[List[Dict]], seat_map: List[str]) -> List[Dict]:
    """Assign seats attempting to place each group in neighboring seats.
    seat_map: flat list of seat identifiers (e.g., ['1A','1B',...]) assumed ordered by adjacency.
    Returns flat passenger list with 'seat_number' assigned where possible.
    """
    assigned = []
    free = list(seat_map)
    for grp in groups:
        size = len([p for p in grp if not p.get('infant')])
        # try to find contiguous block of size
        found_block = None
        for i in range(len(free)-size+1):
            block = free[i:i+size]
            # accept any contiguous block
            if len(block) == size:
                found_block = (i, block)
                break
        if found_block:
            idx, block = found_block
            # assign seats to non-infants
            bi = 0
            for p in grp:
                if p.get('infant'):
                    p['seat_number'] = None
                else:
                    p['seat_number'] = block[bi]
                    bi += 1
            # remove used seats
            for _ in range(size):
                free.pop(0)
        else:
            # fallback: assign any available seats
            for p in grp:
                if p.get('infant'):
                    p['seat_number'] = None
                else:
                    if free:
                        p['seat_number'] = free.pop(0)
                    else:
                        p['seat_number'] = None
        assigned.extend(grp)
    return assigned
