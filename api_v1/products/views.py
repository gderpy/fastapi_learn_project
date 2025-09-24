from fastapi import APIRouter, HTTPException, status

from . import crud
from .schemas import Product, ProductCreate


router = APIRouter(tags=["Products"])

# Для эндпоинтов добавлен response_model: list[Product], Product
# Теперь FastAPI будет автоматически валидировать и возвращать объекты в нужном формате

@router.get("/", response_model=list[Product])
async def get_products(session):
    return await crud.get_products(session)


@router.post("/", response_model=Product)
async def create_product(session, product_in: ProductCreate):
    return await crud.create_product(session=session, product_in=product_in)


@router.get("/{product_id}/", response_model=Product)
async def get_product(session, product_id: int):
    product = await crud.get_product(session=session, product_id=product_id)

    if product is not None:
        return product
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Product {product_id} not found!"
    )

