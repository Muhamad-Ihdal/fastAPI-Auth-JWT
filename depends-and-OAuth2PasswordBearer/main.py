from fastapi import FastAPI,HTTPException
from schemas import UserRegister,UserResponse
from jose import jwt,JWTError
from auth import verify_password,hash_password
from db import add_user,get_user_by_id
app = FastAPI()

def error(status_code=401,massage="not valid"):
    raise HTTPException(
        status_code=status_code,
        detail={
            "success":False,
            "massage":massage
        }
    )


@app.post("/register")
def register(user: UserRegister):
    # user = user.model_dump()
    add = add_user(user.email,hash_password(user.password))
    if not add:
        error(massage="Email telah digunakan")
    