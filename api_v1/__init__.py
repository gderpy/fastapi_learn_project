from fastapi import APIRouter 

from .products.views import router as products_router
from .demo_auth.views import router as demo_auth_router


router = APIRouter()
# теперь все ручки из products будут доступны под /products
# собирает все эндпоинты модуля products в один общий роутер.
router.include_router(router=products_router, prefix="/products")
router.include_router(router=demo_auth_router)