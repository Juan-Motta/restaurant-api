from fastapi import APIRouter

from src.infraestructure.adapters.input.api.auth import router as auth_router
from src.infraestructure.adapters.input.api.menu_item import router as menu_item_router
from src.infraestructure.adapters.input.api.order import router as order_router
from src.infraestructure.adapters.input.api.order_item import (
    router as order_item_router,
)
from src.infraestructure.adapters.input.api.rating import router as rating_router
from src.infraestructure.adapters.input.api.restaurant import (
    router as restaurant_router,
)
from src.infraestructure.adapters.input.api.root import router as root_router
from src.infraestructure.adapters.input.api.user import router as user_router

router_v1 = APIRouter(prefix="/api/v1")

router_v1.include_router(root_router)
router_v1.include_router(auth_router)
router_v1.include_router(restaurant_router)
router_v1.include_router(user_router)
router_v1.include_router(menu_item_router)
router_v1.include_router(order_router)
router_v1.include_router(order_item_router)
router_v1.include_router(rating_router)

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
    {
        "name": "Orders",
        "description": """Endpoints to manage orders""",
    },
    {
        "name": "Order Items",
        "description": """Endpoints to manage order items""",
    },
    {
        "name": "Ratings",
        "description": """Endpoints to manage ratings""",
    },
    {
        "name": "Authentication",
        "description": """Endpoints to manage authentication""",
    },
]
