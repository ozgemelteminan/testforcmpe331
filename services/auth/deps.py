# services/auth/deps.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import os
from typing import List # EKLENDİ

SECRET_KEY = os.environ.get('CMPE331_SECRET', 'CHANGE_THIS_SECRET')
ALGORITHM = 'HS256'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')

# MEVCUT FONKSİYON (Değişmedi - Sadece token geçerli mi diye bakar)
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    # DÜZELTME: Token'dan tam kullanıcı bilgisini döndür
    return {"username": username, "roles": payload.get("roles", [])}


# --- YENİ FONKSİYON EKLENDİ ---
# (Sadece token'ın geçerli değil, aynı zamanda "admin" rolüne sahip olup
# olmadığını da kontrol eder)
def get_current_admin_user(current_user: dict = Depends(get_current_user)):
    """
    Mevcut kullanıcıyı alır ve 'admin' rolüne sahip olup olmadığını kontrol eder.
    Eğer 'admin' rolü yoksa 403 Forbidden hatası fırlatır.
    """
    user_roles: List[str] = current_user.get("roles", [])
    
    if "admin" not in user_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted. Admin rights required."
        )
    
    return current_user
