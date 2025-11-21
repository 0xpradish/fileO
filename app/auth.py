from fastapi.security import APIKeyHeader

from fastapi import APIRouter, Depends, HTTPException
from jose import jwt, JWTError

from dotenv import load_dotenv
import os
load_dotenv()



EMAIL = os.getenv("EMAIL") 
PASSWORD = os.getenv("PASSWORD") 

SECRET_KEY = str(os.getenv("SECRET"))

ALGORITHM = "HS256"

api_key_header = APIKeyHeader(name="Authorization")



def get_current_user(token: str = Depends(api_key_header)):
    if not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    token = token.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")