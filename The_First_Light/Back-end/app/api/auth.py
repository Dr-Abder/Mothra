from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, constr, Field
from enum import Enum
router = APIRouter()


class SexEnum(str, Enum):
    male = "male"
    female = "female"

class Signup(BaseModel):
    first_name: constr(regex="^[A-Za-z]+$", min_length=1) 
    last_name: constr(regex="^[A-Za-z]+$", min_length=1)
    email: EmailStr
    password: constr(regex="^(?=.*?[A-Za-z])(?=.*?\d)(?=.*?[#?!@$%^&*-]).+$", min_length=8)
    age: int = Field(..., ge=0)
    sex: SexEnum

@router.post("/signup")
async def create_auth(signup: Signup):
    return ("user created")

class Login(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
async def login_auth(login: Login):
    return ("user connected")