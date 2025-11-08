
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
pwd = CryptContext(schemes=['bcrypt'], deprecated='auto')
SECRET = 'replace-this-secret'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='users/token')

# demo user
_fake = {'admin': {'username': 'admin', 'hashed': pwd.hash('password')}}

def authenticate_user(username, password):
    u = _fake.get(username)
    if not u: return None
    if not pwd.verify(password, u['hashed']):
        return None
    return u

def create_access_token(data: dict, expires_minutes: int = 60*24):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({'exp': expire})
    token = jwt.encode(to_encode, SECRET, algorithm='HS256')
    return token
