import uuid

from fastapi import APIRouter, HTTPException

from core.security import AdminDep, SessionDep, SuperDep
from api.user.models import Users


router = APIRouter(prefix="/admin", tags=["admin"])


@router.put("/set_user_admin/{id}")
async def set_user_admin(
    *, Session: SessionDep, User: AdminDep, admin: bool, id: uuid.UUID
):
    """allows superuser or admins to give someone admin permissions"""
    db_user = Session.query(Users).filter(Users.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Found")
    db_user.is_admin = admin
    Session.commit()
    return {"data": "User Is Now Admin"}


@router.put("/set_user_permissions/{id}")
async def set_user_permissions(
    *,
    Session: SessionDep,
    User: SuperDep,
    id: uuid.UUID,
    admin: bool | None,
    superuser: bool | None,
):
    """Sets permissions for any user"""
    """Only permitted for superuser"""
    db_user = Session.query(Users).filter(Users.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Found")
    db_user.is_admin = admin
    db_user.is_superuser = superuser
    Session.commit()
    return {"data": "User Permissions Updated Successfully"}
