from fastapi import FastAPI,HTTPException,Header
from user import fk_user
from auth import create_token,verify_token

app = FastAPI()

@app.post("/login")
def login(email:str):
    user = fk_user.get(email)
    if not user:
        HTTPException(401,"invalid user")

    token = create_token(user_id=user["id"],email=user["email"])
    return {"access_token":token}

@app.get("/profile")
def profile(authorization:str = Header(None)):
    if authorization is None:
        HTTPException(status_code=401,detail="no token")
    
    token = authorization.replace("Bearer ","")
    user = verify_token(token=token)
    if not user:
        HTTPException(status_code=401,detail="Invalid token")
    
    return {
        "id": user["sub"],
        "email": user["email"]
    }

