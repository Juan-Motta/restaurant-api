from fastapi import APIRouter

from src.infraestructure.adapters.input.api.menu_item import router as menu_item_router
from src.infraestructure.adapters.input.api.order import router as order_router
from src.infraestructure.adapters.input.api.restaurant import (
    router as restaurant_router,
)
from src.infraestructure.adapters.input.api.root import router as root_router
from src.infraestructure.adapters.input.api.user import router as user_router

router_v1 = APIRouter(prefix="/api/v1")

router_v1.include_router(root_router)
router_v1.include_router(restaurant_router)
router_v1.include_router(user_router)
router_v1.include_router(menu_item_router)
router_v1.include_router(order_router)

METADATA = [
    {
        "name": "Restaurants",
        "description": """Endpoints to manage restaurants""",
    },
    {
        "name": "Users",
        "description": """Endpoints to manage users""",
    },
    {
        "name": "Menu Items",
        "description": """Endpoints to manage menu items""",
    },
    {
        "name": "Root",
        "description": """Root endpoint""",
    },
]
