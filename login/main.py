from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,EmailStr
from passlib.context import CryptContext
from db import create_table,add_user,delete_table,user_account
app = FastAPI()
# create_table()
# delete_table()


def error(status_code=400,massage="Data gagal diubah"):
    raise HTTPException(
        status_code=status_code,
        detail={
            "success":False,
            "massage":massage
        })

def berhasil(massage:str = "Proses berhasil"):
    return {
        "success":True,
        "massage":massage
    }


# ------------------------ schemas start
class RegisterRequest(BaseModel):
    email: EmailStr
    password:str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
# ------------------------ schemas end


# ------------------------register start
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_pwd(password:str) -> str:
    return pwd_context.hash(password)

def verify_pwd(plain_password:str,hashed_password:str) -> bool:
    return pwd_context.verify(plain_password,hashed_password)


@app.post("/register")
def regis(user:RegisterRequest):
    email = user.email
    password = hash_pwd(user.password)
    result = add_user(email,password)
    if result == "Email telah digunakan":
        error(status_code=409,massage=result)
    return berhasil(massage=result)

# ------------------------register end


# ------------------------Login start
@app.post("/login")
def login(user:LoginRequest):
    email = user.email
    hashed_password = user_account(email)
    if hashed_password is None:
        error(status_code=401,massage="Invalid email or password")
    if not verify_pwd(user.password,hashed_password):
        error(status_code=401,massage="Invalid email or password")
    
    return berhasil(massage="User berhasil login")
# ------------------------Login end
