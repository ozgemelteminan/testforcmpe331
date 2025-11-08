import os
from fastapi import Header, HTTPException, Depends
def verify_token(x_token: str = Header(None)):
    expected = os.getenv("API_SECRET", "defaultsecret")
    if x_token != expected:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True
