import uuid

from datetime import datetime, timedelta
from typing import Annotated
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from api.user.models import Users
from core.config import JWT_KEY, ALGORITHM
from database import get_db


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/user/login")


def authenticate_user(username: str, password: str, db):
    """Authenticate User by comparing password and hashed password"""
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: str, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id, "exp": datetime.now() + expires_delta}
    return jwt.encode(encode, JWT_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    """Verifies if User is logged in"""
    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Could Not Validate User")

        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Could Not Validate User ( JWT Error )"
        )


async def get_superuser(
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """Used for Superuser Dependency"""
    user = db.query(Users).filter(Users.id == uuid.UUID(current_user["id"])).first()
    if not user or not user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Insufficient Permissions. Superuser access required.",
        )
    return current_user


async def get_admin(
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """Used for Admin Dependency"""
    user = db.query(Users).filter(Users.id == uuid.UUID(current_user["id"])).first()
    if not user or not user.is_admin:
        raise HTTPException(
            status_code=403, detail="Insufficient Permissions. Admin Access Required"
        )
    return current_user


SessionDep = Annotated[Session, Depends(get_db)]
UserDep = Annotated[dict, Depends(get_current_user)]
SuperDep = Annotated[dict, Depends(get_superuser)]
AdminDep = Annotated[dict, Depends(get_admin)]
