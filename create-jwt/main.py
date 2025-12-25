from fastapi import FastAPI,HTTPException,Header
from user import fk_user
from auth import create_token,verify_token

app = FastAPI()

@app.post("/login")
def user_login(email:str):
    user = fk_user.get(email)
    if not user:
        HTTPException(401,"invalid user")

    token = create_token(user_id=user["id"],email=user["email"])
    return {"access_token":token}






















if __name__ == "__main__":
    user_login(email="inisalah@gmail.com")
