import uuid

from datetime import datetime
from fastapi import FastAPI

from database import Base, engine, SessionLocal
from api.routes import router as api_router
from status.status import router as superuser_router
from api.user.models import Users
from core.security import bcrypt_context
from core.config import SUPERUSER_USERNAME, SUPERUSER_PASSWORD


app = FastAPI()
Base.metadata.create_all(bind=engine)


app.include_router(api_router)
app.include_router(superuser_router)


@app.get("/")
async def root():
    return {"data": "App is running"}


def create_superuser():
    """Superuser Creation on startup function"""

    Session = SessionLocal()

    db_superuser = (
        Session.query(Users).filter(Users.username == SUPERUSER_USERNAME).first()
    )
    if db_superuser:
        return {"data": "Superuser Already Exist"}

    db_super = Users(
        id=uuid.uuid4(),
        username=SUPERUSER_USERNAME,
        hashed_password=bcrypt_context.hash(SUPERUSER_PASSWORD),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_admin=True,
        is_superuser=True,
    )

    Session.add(db_super)
    Session.commit()
    return {"data": "Superuser Created Successfully"}


create_superuser()  # generates superuser on backend startup
