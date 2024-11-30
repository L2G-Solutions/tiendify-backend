from pydantic import BaseModel


class CategoryCreate(BaseModel):
    slug: str
    name: str
    description: str
