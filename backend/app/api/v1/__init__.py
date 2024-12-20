from fastapi import APIRouter

from .auth import router as auth_router
from .users import router as users_router
from .priorities import router as priorities_router
from .categories import router as categories_router
from .todos import router as todos_router
from .debug import router as debug_router
from .webhooks import router as webhooks_router
from .websockets import router as websockets_router
from .notifications import router as notifications_router
from app.core.config import get_config


config = get_config()

router = APIRouter(prefix=config.API_V1_STR)

router.include_router(debug_router)
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(priorities_router)
router.include_router(categories_router)
router.include_router(todos_router)

router.include_router(webhooks_router)
router.include_router(websockets_router)
router.include_router(notifications_router)