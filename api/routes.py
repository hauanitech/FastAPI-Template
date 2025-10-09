from fastapi import APIRouter

from api.user.routes import router as user_router
from api.admin.routes import router as super_router


router = APIRouter(prefix="/api")


router.include_router(user_router)
router.include_router(super_router)
