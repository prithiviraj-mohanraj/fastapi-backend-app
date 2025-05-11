from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Literal


class UserCreate(BaseModel):
    email:EmailStr
    password:str

class Responseuser(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        orm_mode: True

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class ResponsePost(PostBase):
    id:int
    created_at:datetime
    owner_id:int
    owner:Responseuser

    class Config:
        orm_mode =True

class PostOut(BaseModel):
    Post: ResponsePost
    votes:int

    class Config:
        orm_mode=True


class Token(BaseModel):
    access_token:str
    token_type:str
class TokenData(BaseModel):
    id : int

class Vote(BaseModel):
    post_id:int
    dir: Literal[0, 1] 