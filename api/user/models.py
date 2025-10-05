from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Boolean

from api.base.models import TableBase


class UserBase(BaseModel):
    username: str = Field(min_length=4, max_length=20)
    password: str = Field(min_length=8, max_length=40)


class UserUpdate(BaseModel):
    username: str | None


class Token(BaseModel):
    access_token: str
    token_type: str


"""DB Model"""


class Users(TableBase):
    __tablename__ = "users"

    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_superuser = Column(Boolean)
    is_admin = Column(Boolean)
