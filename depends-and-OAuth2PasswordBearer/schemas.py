from pydantic import BaseModel,EmailStr
from typing import Optional,Any

class UserRequest(BaseModel):
    email: EmailStr
    password:str
    role:str

class UserResponse(BaseModel):
    id:int
    email: EmailStr

class SuccessResponse(BaseModel):
    success:bool
    massage:str
    data:Optional[Any]   

class LoginResponse(BaseModel):
    access_token:str
    refresh_token:str
    token_type:str

class RefreshRequest(BaseModel):
    refresh_token:str

class RefreshResponse(BaseModel):
    access_token:str
    refresh_token:str
    token_type:str
    