from jose import jwt,JWTError
from datetime import datetime,timedelta,timezone

SECRRET_KEY = "INI_KEY_GW"
ALGORITHM = "HS256"

def create_token(user_id:int ,email:str) -> str:
    payload = {
        "sub" : str(user_id),
        "email":email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5)
    }
    return jwt.encode(payload,SECRRET_KEY,algorithm=ALGORITHM)

def verify_token(token:str):
    try:
        return jwt.decode(token,SECRRET_KEY,algorithms=ALGORITHM)
        # return jwt.decode(token,SECRRET_KEY,algorithms=[ALGORITHM])
    except JWTError:
        return None


if __name__ == "__main__":
    pass
    # x = create_token(user_id=2,email="efadfafdsa")
    # print(type(x))


