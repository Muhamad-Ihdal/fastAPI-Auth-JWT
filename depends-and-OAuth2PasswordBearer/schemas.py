from pydantic import BaseModel,EmailStr

class UserRequest(BaseModel):
    email: EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    email: EmailStr

class SuccessResponse(BaseModel):
    success:bool
    massage:str
    user:UserResponse