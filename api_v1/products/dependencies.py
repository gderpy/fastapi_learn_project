from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Product
from . import crud

# Annotated позволяет добавить к типу переменной дополнительные метаданные.

# Здесь мы используем Path — специальную функцию FastAPI, которая указывает:
# - параметр product_id берётся из пути запроса (например, /products/5)
# - тип этого параметра — int

# Через Path можно также задавать ограничения (min, max, описание и т.д.).
# Такой подход делает сигнатуру функции более явной и удобной для автодополнения и документации.

async def product_by_id(
    product_id: Annotated[int, Path],  # product_id будет взят из URL, например /products/5
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> Product:
    product = await crud.get_product(session=session, product_id=product_id)

    if product is not None:
        return product
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Product {product_id} not found!"
    )