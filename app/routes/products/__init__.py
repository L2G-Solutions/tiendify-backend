from fastapi import APIRouter, Depends, Response

from app.database import get_shops_db
from app.routes.products.utils import (
    parse_products_response_data,
    parse_single_product_response_data,
)
from database.client_shop_db import Prisma as ShopsClient

router = APIRouter(tags=["products"])


@router.get("/")
async def handle_get_products(
    shop_db: ShopsClient = Depends(get_shops_db), limit: int = 20, offset: int = 0
):
    data = await shop_db.products.find_many(
        include={
            "product_categories": {"include": {"categories": True}},
            "products_mediafiles": {"include": {"mediafiles": True}, "take": 1},
        },
        take=limit,
        skip=offset,
    )
    count = await shop_db.products.count()

    return {
        "products": parse_products_response_data(data),
        "total": count,
    }


@router.get("/{product_id}")
async def handle_get_product(
    product_id: int, shop_db: ShopsClient = Depends(get_shops_db)
):
    product = await shop_db.products.find_unique(
        where={"id": product_id},
        include={
            "product_categories": {"include": {"categories": True}},
            "products_mediafiles": {"include": {"mediafiles": True}},
        },
    )

    if not product:
        return Response(status_code=404)

    return parse_single_product_response_data(product)
