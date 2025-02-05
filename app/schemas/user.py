from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    email: str or None = None # type: ignore
    full_name: str or None = None # type: ignore
    disabled: bool or None = None # type: ignore

class UserinDB(User):
    hashed_password: str

# class User(UserBase):
#     id: int

#     class Config:
#         orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str or None = None


