from fastapi import FastAPI,HTTPException,Depends
from jose import jwt,JWTError
from schemas import UserResponse,SuccessResponse,UserRequest,LoginResponse
# from jose import jwt,JWTError
from auth import verify_password,hash_password,create_token_jwt,verify_token_jwt,oauth2_sheme
from db import add_user,get_user_by_id,get_user_by_email,update_data,delete_data
app = FastAPI()

def get_current_user(token = Depends(oauth2_sheme)):
    payload = verify_token_jwt(token=token)
    if not payload:
        error(massage="invalid Token")
    
    user_id = payload.get("sub")
    user = get_user_by_id(int(user_id))

    if not user['success']:
        error(massage=user["massage"])
    return user['data']
    

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

# -------------------------------------------------------- request start

@app.post("/register",response_model=SuccessResponse)
def register(user: UserRequest):
    # user = user.model_dump()
    hasil= add_user(user.email,hash_password(user.password))
    if not hasil["success"]:
        error(massage=hasil["massage"])

    return berhasil(massage=hasil["massage"],data=hasil["data"])

@app.post("/login",response_model=LoginResponse)
def login(user:UserRequest):
    hasil = get_user_by_email(user.email)
    
    success = hasil["success"]
    massage = hasil["massage"]
    data = hasil["data"]
    if not success:
        error(massage="invalid email or password")
    
    if not verify_password(plain_password=user.password,hashed_password=data["password"]):
        error(massage="invalid email or password")

    token = create_token_jwt(user_id=data["id"],email=data["email"])

    return {
        "success":True,
        "massage":"login berhasil",
        "data":data,
        "access_token":token
    }
    
@app.get("/profile",response_model=UserResponse)
def profile(user = Depends(get_current_user)):
    return user

@app.put("/profile",response_model=SuccessResponse)
def update_profile(new_profile:UserRequest,current_user = Depends(get_current_user)):
    new_hashed_password = hash_password(new_profile.password)
    hasil = update_data(
        user_id=current_user["id"],
        new_email=new_profile.email,
        new_password=new_hashed_password)
    success = hasil["success"]
    if not success:
        error(massage=hasil["massage"])
    
    return berhasil(massage="Profile berhasil di update",data=hasil["data"])
    
@app.delete("/profile",response_model=SuccessResponse)
def delete_user(current_user=Depends(get_current_user)):
    hasil = delete_data(user_id=current_user["id"])
    if not hasil["success"]:
        error(status_code=400,massage=hasil["massage"])
        
    return berhasil(massage=" data User berhasil di hapus",data=current_user)

    


    
# -------------------------------------------------------- request end