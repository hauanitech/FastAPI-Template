import uuid

from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.user.models import UserBase, Users, Token, UserUpdate
from core.security import (
    bcrypt_context,
    authenticate_user,
    create_access_token,
    SessionDep,
    SuperDep,
    UserDep
)
from core.config import SUPERUSER_PASSWORD, SUPERUSER_USERNAME


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register_user")
async def register_user(*, Session: SessionDep, user: UserBase):
    user_db = Users(
        id=uuid.uuid4(),
        username=user.username,
        hashed_password=bcrypt_context.hash(user.password),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_admin=False,
        is_superuser=False,
    )
    if user.username == SUPERUSER_USERNAME and user.password == SUPERUSER_PASSWORD:
        user_db.is_superuser = True
    Session.add(user_db)
    Session.commit()
    return {"data": "User Created Successfully"}


@router.post("/login", response_model=Token)
async def login_for_access_token(
    *, Session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(form_data.username, form_data.password, Session)

    if not user:
        raise HTTPException(status_code=401, detail="Could Not Authenticate User")

    token = create_access_token(user.username, str(user.id), timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}


@router.get("/get_current_user")
async def get_current_user(*, Session: SessionDep, User: UserDep):
    user_db = Session.query(Users).filter(Users.id == uuid.UUID(User["id"])).first()
    return user_db


@router.get("/get_users")
async def get_users(
    *,
    Session: SessionDep,
    User: SuperDep,
    is_superuser: bool | None,
    is_admin: bool | None
):
    return Session.query(Users).filter(is_superuser == is_superuser and is_admin == is_admin).all()


@router.get("/get_user_by_id/{user_id}")
async def get_user_by_id(
    *,
    Session: SessionDep,
    User: SuperDep,
    user_id = uuid.UUID
):
    db_user = Session.query(Users).filter(Users.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return {"data" : db_user}


@router.put("/update_my_username")
async def update_my_username(
    *,
    Session: SessionDep,
    User: UserDep,
    data: UserUpdate
):
    db_user = Session.query(Users).filter(Users.id == uuid.UUID(User["id"])).first()
    db_user.username = data.username
    Session.commit()
    return {"data" : "Username Updated Successfully"}


@router.put("/update_user_by_id/{user_id}")
async def update_user_by_id(
    *,
    Session: SessionDep,
    User: SuperDep,
    user_id: uuid.UUID
):
    db_user = Session.query(Users).filter(Users.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return {"data" : db_user}


@router.delete("/delete_user/{user_id}")
async def delete_user(
    *,
    Session: SessionDep,
    User: SuperDep,
    user_id: uuid.UUID
):
    db_user = Session.query(Users).filter(Users.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Found")
    if db_user.is_superuser:
        raise HTTPException(status_code=401, detail="Not Deletable User")
    
    Session.delete(db_user)
    Session.commit()
    return {"data" : "User Deleted Successfully"}