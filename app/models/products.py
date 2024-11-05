from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    price: float
    description: str
    stock: int
    categories: list[str]
