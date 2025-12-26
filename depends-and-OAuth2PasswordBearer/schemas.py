from pydantic import BaseModel,EmailStr

class UserRegister(BaseModel):
    email: EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    email: EmailStr
    