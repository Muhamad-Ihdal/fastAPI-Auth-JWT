from passlib.context import CryptContext
from jose import jwt,JWTError,ExpiredSignatureError
from datetime import datetime,timedelta,timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from db import get_user_by_id

oauth2_sheme = OAuth2PasswordBearer(tokenUrl="login")

# ------------------------------- Hash start
pwd_contex = CryptContext(
    schemes=['bcrypt'],
    deprecated="auto"
)

def hash_password(password:str) -> str:
    return pwd_contex.hash(password)

def verify_password(plain_password:str,hashed_password:str) -> bool:
    return pwd_contex.verify(plain_password,hashed_password)

# ------------------------------- Hash end

# ------------------------------- jwt start

SECRET_KEY = "INI_CONTOH_AJA"
ALGORITHM = "HS256"

def create_access_token(user_id:int,email:str) -> str:
    payload = {
        "sub":str(user_id),
        "email":email,
        "type":"access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15)
    }
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)


def create_refresh_token(user_id:int) -> str:
    payload = {
        "sub":str(user_id),
        "type":"refresh",
        "exp": datetime.now(timezone.utc) + timedelta(days=7)
    }
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

def verify_token_jwt(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    except JWTError:
        return None
    return payload

# ------------------------------- jwt end
