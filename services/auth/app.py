# services/auth/app.py

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
import os
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone # EKLENDİ
from pydantic import BaseModel # EKLENDİ

app = FastAPI()
SECRET_KEY = os.environ.get('CMPE331_SECRET', 'CHANGE_THIS_SECRET')
ALGORITHM = 'HS256'
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- YENİ EKLENDİ: Token Süreleri ---
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Access token 30 dakika geçerli
REFRESH_TOKEN_EXPIRE_DAYS = 7     # Refresh token 7 gün geçerli

# --- YENİ EKLENDİ: Refresh endpoint'i için Pydantic modeli ---
class TokenRefreshRequest(BaseModel):
    refresh: str

# DÜZELTME 1: Kullanıcı veritabanına "roles" alanı eklendi
USERS = {
    "admin": {
        "username": "admin",
        "password": pwd_context.hash("adminpass"),
        "roles": ["admin", "user"] # Admin hem admin hem user
    },
    "user_ozge": {
        "username": "user_ozge",
        "password": pwd_context.hash("userpass"),
        "roles": ["user"] # Bu kullanıcı sadece 'user'
    }
}

# --- YENİ EKLENDİ: Token yaratmak için yardımcı fonksiyon ---
def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- DÜZELTME: 'login' fonksiyonu artık 'refresh_token' da üretiyor ---
@app.post('/auth/token')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = USERS.get(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user['password']):
        raise HTTPException(status_code=400, detail='Incorrect username or password')
    
    # Access token için payload (roller dahil, kısa ömürlü)
    access_payload = {
        "sub": user['username'],
        "roles": user.get("roles", [])
    }
    access_token = create_token(
        data=access_payload,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    # Refresh token için payload (rol yok, sadece kimlik, uzun ömürlü)
    refresh_payload = {
        "sub": user['username']
        # Roller buraya EKLENMEMELİ. Refresh token sadece kimlik yeniler.
    }
    refresh_token = create_token(
        data=refresh_payload,
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    
    # Dökümandaki gibi access ve refresh token döndür
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# --- YENİ EKLENDİ: Refresh Token Endpoint'i ---
# (Arkadaşınızın dökümanındaki POST /api/token/refresh/)
@app.post('/auth/token/refresh')
def refresh_access_token(payload: TokenRefreshRequest):
    token = payload.refresh
    try:
        # Refresh token'ı decode et (süre dolmamışsa)
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        username: str = decoded_payload.get('sub')
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid refresh token')
        
        # Token'daki kullanıcı hala sistemde var mı?
        user = USERS.get(username)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

        # Yeni bir ACCESS token oluştur (kısa ömürlü, roller dahil)
        new_access_payload = {
            "sub": user['username'],
            "roles": user.get("roles", [])
        }
        new_access_token = create_token(
            data=new_access_payload,
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {"access_token": new_access_token, "token_type": "bearer"}

    except JWTError:
        # Token geçersiz veya süresi dolmuş
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid or expired refresh token'
        )
