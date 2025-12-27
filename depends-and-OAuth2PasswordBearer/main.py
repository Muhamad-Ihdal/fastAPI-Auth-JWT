from fastapi import FastAPI,HTTPException,Depends
from schemas import UserResponse,SuccessResponse,UserRequest
from jose import jwt,JWTError
from auth import verify_password,hash_password
from db import add_user,get_user_by_id,get_user_by_email
app = FastAPI()

def error(status_code=401,massage="not valid"):
    raise HTTPException(
        status_code=status_code,
        detail={
            "success":False,
            "massage":massage,
            "data":None
        }
    )

def berhasil(massage="Proses berhasil",data={}):
    return {
        "success":True,
        "massage":massage,
        "data":data
    }

@app.post("/register",response_model=SuccessResponse)
def register(user: UserRequest):
    # user = user.model_dump()
    hasil= add_user(user.email,hash_password(user.password))
    if not hasil["success"]:
        error(massage=hasil["massage"])

    return berhasil(massage=hasil["massage"],user=hasil["data"])

@app.post("/login")
def login(user:UserRequest):
    hasil = get_user_by_email(user.email)
    success = hasil["success"]
    massage = hasil["massage"]
    data = hasil["data"]
    if not success:
        error(massage=massage)

    