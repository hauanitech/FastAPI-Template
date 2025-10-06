from fastapi import APIRouter

from core.security import SessionDep
from core.config import SUPERUSER_USERNAME
from api.user.models import Users


router = APIRouter(prefix="/status", tags=["status"])


@router.get("/superuser_status")
async def superuser_status(*, Session: SessionDep):
    db_super = Session.query(Users).filter(Users.username == SUPERUSER_USERNAME).first()
    if not db_super:
        return {"data": "Superuser Does Not Exist in Database"}

    return {"data": "Superuser Exist in the database"}
