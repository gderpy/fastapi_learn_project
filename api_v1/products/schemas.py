from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    price: int


class ProductCreate(BaseModel):
    pass 


class Product(ProductBase):
    id: int