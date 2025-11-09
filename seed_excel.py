import pandas as pd
import httpx
import json
import math

# --- AYARLAR ---
BASE_URL = "http://127.0.0.1"
AUTH_URL = f"{BASE_URL}:8005/auth/token"
FLIGHT_API_URL = f"{BASE_URL}:8004/flights/"
PILOT_API_URL = f"{BASE_URL}:8001/pilots/"
CABIN_API_URL = f"{BASE_URL}:8002/attendants/"
PASSENGER_API_URL = f"{BASE_URL}:8003/passengers/"

EXCEL_FILE = "veri.xlsx"
ADMIN_USER = "admin"
ADMIN_PASS = "adminpass"
# -----------------

def get_admin_token():
    """Önce admin token'ı alır."""
    print("Admin token alınıyor...")
    try:
        r = httpx.post(AUTH_URL, data={"username": ADMIN_USER, "password": ADMIN_PASS})
        r.raise_for_status()
        token_data = r.json()
        print("Token başarıyla alındı.")
        return token_data["access_token"]
    except Exception as e:
        print(f"Token alınamadı! Hata: {e}")
        return None

def clean_value(value):
    """Pandas'tan gelen 'nan' (boş hücre) değerlerini None yapar."""
    if pd.isna(value):
        return None
    # Excel'den gelen 1.0 gibi sayıları int'e çevirir
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value

def parse_json_string(value):
    """Excel'deki '[""a"",""b""]' gibi bir string'i JSON listesine çevirir."""
    val = clean_value(value)
    if val is None:
        return None
    try:
        # Excel'den gelen string'i (örn: '[""a""]') düzelt
        corrected_string = val.replace('""', '"')
        return json.loads(corrected_string)
    except (json.JSONDecodeError, TypeError):
        print(f"Uyarı: JSON listesi okunamadı: {val}")
        return None

def seed_data(token):
    if not token:
        return

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    client = httpx.Client(headers=headers, timeout=10.0)

    # 1. UÇUŞLARI YÜKLE (FLIGHTS)
    try:
        df_flights = pd.read_excel(EXCEL_FILE, sheet_name="Flights")
        print(f"\n--- {len(df_flights)} adet Uçuş (Flight) yükleniyor... ---")
        for _, row in df_flights.iterrows():
            payload = {
                "flight_number": clean_value(row.get("flight_number")),
                "departure": {
                    "country": clean_value(row.get("departure_country")),
                    "city": clean_value(row.get("departure_city")),
                    "airport_name": clean_value(row.get("departure_airport_name")),
                    "airport_code": clean_value(row.get("departure_airport_code"))
                },
                "arrival": {
                    "country": clean_value(row.get("arrival_country")),
                    "city": clean_value(row.get("arrival_city")),
                    "airport_name": clean_value(row.get("arrival_airport_name")),
                    "airport_code": clean_value(row.get("arrival_airport_code"))
                },
                "datetime": clean_value(row.get("datetime")),
                "duration_minutes": clean_value(row.get("duration_minutes")),
                "distance": clean_value(row.get("distance")),
                "vehicle_type": clean_value(row.get("vehicle_type")),
                "max_passengers": clean_value(row.get("max_passengers")),
                "max_crew": clean_value(row.get("max_crew"))
            }
            try:
                r = client.post(FLIGHT_API_URL, json=payload)
                r.raise_for_status()
                print(f"Başarılı: Uçuş '{payload['flight_number']}' eklendi.")
            except httpx.HTTPStatusError as e:
                print(f"HATA: Uçuş '{payload.get('flight_number')}' eklenemedi. Sunucu: {e.response.text}")
    except Exception as e:
        print(f"'Flights' sayfası okunurken hata: {e}")

    # 2. PİLOTLARI YÜKLE (PILOTS)
    try:
        df_pilots = pd.read_excel(EXCEL_FILE, sheet_name="Pilots")
        print(f"\n--- {len(df_pilots)} adet Pilot yükleniyor... ---")
        for _, row in df_pilots.iterrows():
            payload = {
                "name": clean_value(row.get("name")),
                "age": clean_value(row.get("age")),
                "seniority": clean_value(row.get("seniority")),
                "vehicle_restriction": clean_value(row.get("vehicle_restriction")),
                "allowed_range": clean_value(row.get("allowed_range")),
                "known_languages": parse_json_string(row.get("known_languages"))
            }
            payload_clean = {k: v for k, v in payload.items() if v is not None}
            try:
                r = client.post(PILOT_API_URL, json=payload_clean)
                r.raise_for_status()
                print(f"Başarılı: Pilot '{payload_clean['name']}' eklendi.")
            except httpx.HTTPStatusError as e:
                print(f"HATA: Pilot '{payload_clean.get('name')}' eklenemedi. Sunucu: {e.response.text}")
    except Exception as e:
        print(f"'Pilots' sayfası okunurken hata: {e}")

    # 3. KABİN EKİBİNİ YÜKLE (CABIN CREW)
    try:
        df_cabin = pd.read_excel(EXCEL_FILE, sheet_name="CabinCrew")
        print(f"\n--- {len(df_cabin)} adet Kabin Ekibi (CabinCrew) yükleniyor... ---")
        for _, row in df_cabin.iterrows():
            payload = {
                "name": clean_value(row.get("name")),
                "age": clean_value(row.get("age")),
                "attendant_type": clean_value(row.get("attendant_type")),
                "seniority": clean_value(row.get("seniority")),
                "chef_recipes": parse_json_string(row.get("chef_recipes")),
                "vehicle_restriction": parse_json_string(row.get("vehicle_restriction"))
            }
            payload_clean = {k: v for k, v in payload.items() if v is not None}
            try:
                r = client.post(CABIN_API_URL, json=payload_clean)
                r.raise_for_status()
                print(f"Başarılı: Kabin Ekibi '{payload_clean['name']}' eklendi.")
            except httpx.HTTPStatusError as e:
                print(f"HATA: Kabin Ekibi '{payload_clean.get('name')}' eklenemedi. Sunucu: {e.response.text}")
    except Exception as e:
        print(f"'CabinCrew' sayfası okunurken hata: {e}")

    # 4. YOLCULARI YÜKLE (PASSENGERS)
    try:
        df_pax = pd.read_excel(EXCEL_FILE, sheet_name="Passengers")
        print(f"\n--- {len(df_pax)} adet Yolcu (Passenger) yükleniyor... ---")
        for _, row in df_pax.iterrows():
            payload = {
                "flight_id": clean_value(row.get("flight_id")),
                "name": clean_value(row.get("name")),
                "age": clean_value(row.get("age")),
                "seat_type": clean_value(row.get("seat_type")),
                "affiliated_ids": parse_json_string(row.get("affiliated_ids")),
                "infant": None
            }
            
            # Bebek bilgisi varsa, 'infant' objesini oluştur
            infant_age = clean_value(row.get("infant_age_months"))
            infant_parent = clean_value(row.get("infant_with_parent_id"))
            if infant_age is not None:
                payload["infant"] = {"age_months": int(infant_age), "with_parent_id": int(infant_parent) if infant_parent else None}

            payload_clean = {k: v for k, v in payload.items() if v is not None}
            try:
                r = client.post(PASSENGER_API_URL, json=payload_clean)
                r.raise_for_status()
                print(f"Başarılı: Yolcu '{payload_clean['name']}' eklendi.")
            except httpx.HTTPStatusError as e:
                print(f"HATA: Yolcu '{payload_clean.get('name')}' eklenemedi. Sunucu: {e.response.text}")
    except Exception as e:
        print(f"'Passengers' sayfası okunurken hata: {e}")

    client.close()
    print("\n--- Veri Yükleme (Seed) İşlemi Tamamlandı! ---")

# --- Script'i Çalıştır ---
if __name__ == "__main__":
    admin_token = get_admin_token()
    seed_data(admin_token)
