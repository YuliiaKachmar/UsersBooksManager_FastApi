from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    surname: str
    email: str
    country: Optional[str]
    password: str
    is_admin: bool


class UserCreate(UserBase):
    pass


class UserLogIn(BaseModel):
    email: str
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


