from fastapi import FastAPI,HTTPException
from schemas import UserRegister,UserResponse,SuccessResponse
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

def berhasil(massage="Proses berhasil",user={}):
    return {
        "success":True,
        "massage":massage,
        "user":user
    }

@app.post("/register",response_model=SuccessResponse)
def register(user: UserRegister):
    # user = user.model_dump()
    user_data = add_user(user.email,hash_password(user.password))
    if not user_data:
        error(massage="Email telah digunakan")

    return berhasil(massage="Register berhasil",user=user_data)