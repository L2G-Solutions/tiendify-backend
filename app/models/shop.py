from enum import Enum
from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class ShopCreate(BaseModel):
    name: str
    headline: Optional[str] = None
    about: Optional[str] = None
    currency: str
    logoimg: Optional[str] = None
    bannerimg: Optional[str] = None
    country: str
    status: str
    verified: bool
    owner_id: UUID
