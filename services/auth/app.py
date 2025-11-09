# services/auth/app.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
import os
from passlib.context import CryptContext

app = FastAPI()
SECRET_KEY = os.environ.get('CMPE331_SECRET', 'CHANGE_THIS_SECRET')
ALGORITHM = 'HS256'
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

@app.post('/auth/token')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = USERS.get(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user['password']):
        raise HTTPException(status_code=400, detail='Incorrect username or password')
    
    # DÜZELTME 2: Token içeriğine (payload) roller eklendi
    payload_data = {
        "sub": user['username'],
        "roles": user.get("roles", []) # Kullanıcının rollerini al
    }
    
    token = jwt.encode(payload_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
