from typing import Dict, Optional
VEHICLES = {
    "A320": {"rows":30,"layout":["A","B","C","D","E","F"],"business_rows": list(range(1,6))},
    "B737": {"rows":28,"layout":["A","B","C","D","E","F"],"business_rows": list(range(1,5))},
    "A330": {"rows":40,"layout":["A","B","C","D","E","F","G","H"],"business_rows": list(range(1,8))},
}
def generate_seat_map_for(vehicle_type: str) -> Optional[Dict]:
    vm = VEHICLES.get(vehicle_type)
    if not vm: return None
    seats = []
    for r in range(1, vm['rows'] + 1):
        for s in vm['layout']:
            seat_id = f"{r}{s}"
            seats.append({"seat_id": seat_id, "row": r, "type": "business" if r in vm['business_rows'] else "economy", "occupied": False})
    return {"seats": seats, "layout": vm}
