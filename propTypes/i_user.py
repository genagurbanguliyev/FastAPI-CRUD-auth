from typing import Optional
from pydantic import BaseModel, Field


class IUser(BaseModel):
    id: Optional[int] = Field(default=None, title="id is not needed")
    username: str = Field(min_length=3)
    email: str = Field(min_length=6)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    password: str
    role: str
    phone_number: str

    class Config:
        json_schema_extra = {
            'example': {
                'username': "gena",
                'email': "genagurbanguliyev@gmail.com",
                'first_name': "Geldimyrat",
                'last_name': "Gurbanguliyev",
                'password': "12345678",
                'role': "admin"
            }
        }


class ITokenToUser(BaseModel):
    username: str
    id: int | None
    role: str


class IUserPassVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)
