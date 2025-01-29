from typing import Optional

from pydantic import BaseModel


class ShopCreate(BaseModel):
    name: str
    headline: Optional[str] = None
    about: Optional[str] = None
    currency: str
    country: str
