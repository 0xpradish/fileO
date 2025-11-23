from fastapi import  HTTPException, Depends, APIRouter
from jose import jwt
from pydantic import BaseModel

from ..auth import EMAIL,PASSWORD, SECRET_KEY, ALGORITHM, get_current_user


class LoginRequest(BaseModel):
    email: str
    password: str


router = APIRouter()

@router.post("/login")
def login(req: LoginRequest):
    if req.email != EMAIL or req.password != PASSWORD:
        print(EMAIL)
        print(PASSWORD)
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode({"sub": req.email}, SECRET_KEY, algorithm=ALGORITHM)
    return {"token": token}



@router.get("/me")
def me(email: str = Depends(get_current_user)):
    return {"logged_in_as": email}
