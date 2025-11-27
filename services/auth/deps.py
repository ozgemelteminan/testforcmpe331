# services/auth/deps.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import os
from typing import List

SECRET_KEY = os.environ.get('CMPE331_SECRET', 'CHANGE_THIS_SECRET')
ALGORITHM = 'HS256'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='http://localhost:8005/auth/token')

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # DÜZELTME: jwt.decode() artık sürenin dolup dolmadığını (exp)
        # otomatik olarak kontrol eder ve süresi dolduysa JWTError fırlatır.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        username: str = payload.get('sub')
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials (no sub)')
            
    except JWTError as e:
        # DÜZELTME: Hata mesajı netleştirildi
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Invalid or expired token. ({str(e)})'
        )
        
    return {"username": username, "roles": payload.get("roles", [])}


# --- 'get_current_admin_user' FONKSİYONU (Değişiklik yok) ---
# (Bu fonksiyon zaten 'get_current_user'a bağımlı olduğu için
# süre dolma kontrolü otomatik olarak ona da uygulanmış olur.)
def get_current_admin_user(current_user: dict = Depends(get_current_user)):
    user_roles: List[str] = current_user.get("roles", [])
    
    if "admin" not in user_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted. Admin rights required."
        )
    
    return current_user
