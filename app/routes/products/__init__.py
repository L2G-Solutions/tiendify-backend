from uuid import uuid4

from fastapi import APIRouter, Depends, Response, UploadFile

from app.database import get_shops_db
from app.models.products import ProductCreate
from app.routes.products.utils import (
    parse_products_response_data,
    parse_single_product_response_data,
)
from app.services.storage import upload_file
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


@router.post("/")
async def handle_create_product(
    data: ProductCreate, shop_db: ShopsClient = Depends(get_shops_db)
):
    new_product = await shop_db.products.create(
        data={
            "name": data.name,
            "description": data.description,
            "stock": data.stock,
            "price": int(data.price),
            "product_categories": {
                "create": [{"category_id": c} for c in data.categories]
            },
        },
        include={
            "product_categories": {"include": {"categories": True}},
            "products_mediafiles": {"include": {"mediafiles": True}},
        },
    )
    return parse_single_product_response_data(new_product)


@router.put("/{product_id}")
async def handle_update_product(
    product_id: int, data: ProductCreate, shop_db: ShopsClient = Depends(get_shops_db)
):
    await shop_db.product_categories.delete_many(
        where={"product_id": product_id, "category_id": {"not_in": data.categories}}
    )
    updated_product = await shop_db.products.update(
        where={"id": product_id},
        data={
            "name": data.name,
            "description": data.description,
            "stock": data.stock,
            "price": int(data.price),
            "product_categories": {
                "create": [{"category_id": c} for c in data.categories]
            },
        },
        include={
            "product_categories": {"include": {"categories": True}},
            "products_mediafiles": {"include": {"mediafiles": True}},
        },
    )

    if updated_product is None:
        return Response(status=404)

    return parse_single_product_response_data(updated_product)


@router.delete("/{product_id}")
async def handle_delete_product(
    product_id: int, shop_db: ShopsClient = Depends(get_shops_db)
):
    deleted_product = await shop_db.products.delete(where={"id": product_id})

    if deleted_product is None:
        return Response(status=404)

    return Response(status=204)


@router.post("/{product_id}/mediafile")
async def handle_create_product_mediafile(
    product_id: int, mediafile: UploadFile, shop_db: ShopsClient = Depends(get_shops_db)
):
    id_ = str(uuid4())

    upload_file(mediafile.file, "products/" + id_)

    new_mediafile = await shop_db.mediafiles.create(
        data={
            "url": "products/" + id_,
            "type": mediafile.content_type if mediafile.content_type else "image/jpeg",
        }
    )

    await shop_db.products_mediafiles.create(
        data={"product_id": product_id, "mediafile_id": new_mediafile.id}
    )

    return new_mediafile
