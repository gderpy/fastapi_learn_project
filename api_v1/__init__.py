from fastapi import APIRouter 

from .products.views import router as products_router


router = APIRouter()
# теперь все ручки из products будут доступны под /products
# собирает все эндпоинты модуля products в один общий роутер.
router.include_router(router=products_router, prefix="/products")