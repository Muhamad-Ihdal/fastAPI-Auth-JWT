from fastapi import FastAPI,HTTPException
from schemas import UserRegister,UserResponse
from jose import jwt,JWTError
from passlib.context import CryptContext
app = FastAPI()


@app.post("/register")
def login(user: UserRegister):
    user = user.model_dump()

    