
# Quick seed script to populate demo services (run after starting the services)
import requests, time
SERVICES = {
    'flight': 'http://localhost:8001/flights',
    'pilot': 'http://localhost:8002/pilots',
    'cabin': 'http://localhost:8003/attendants',
    'passenger': 'http://localhost:8004/passengers'
}
# seed flight
requests.post(SERVICES['flight'], json={
    'flight_number': 'AA1234', 'datetime': '2025-11-09T10:00:00', 'distance_km': 1200, 'vehicle_type': 'A320'
})
# pilots
requests.post(SERVICES['pilot'], json={'id':'P1','name':'Alice','seniority':'senior','vehicle_restriction':'A320'})
requests.post(SERVICES['pilot'], json={'id':'P2','name':'Bob','seniority':'junior','vehicle_restriction':'A320'})
# attendants
for i in range(1,6):
    requests.post(SERVICES['cabin'], json={'id':f'A{i}','name':f'Att{i}','attendant_type':'regular','vehicle_restrictions':['A320']})
# passengers
for i in range(1,21):
    requests.post(SERVICES['passenger'], json={'id':f'PS{i}','flight_number':'AA1234','name':f'Passenger {i}','age':30,'seat_type':'economy' if i>3 else 'business'})
print('seed done')
