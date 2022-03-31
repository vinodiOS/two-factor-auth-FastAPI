import email
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    secret: str

class ShowUser(BaseModel):
    email: str

    class Config:  # to convert non dict obj to json
        orm_mode = True