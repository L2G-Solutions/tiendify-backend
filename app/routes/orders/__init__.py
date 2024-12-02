from fastapi import APIRouter, Depends, Response

from app.constants import PaymentStatus, ShippingStatus
from app.database import get_shops_db
from database.client_shop_db import Prisma as ShopsClient

router = APIRouter(tags=["orders"])


@router.get("/")
async def handle_get_orders(
    shop_db: ShopsClient = Depends(get_shops_db),
    limit: int = 20,
    offset: int = 0,
):
    data = await shop_db.orders.find_many(
        take=limit,
        skip=offset,
        order={"ordered_at": "desc"},
        include={"payments": True, "shipping": True},
    )

    return data


@router.get("/{order_id}")
async def handle_get_order(
    order_id: int,
    shop_db: ShopsClient = Depends(get_shops_db),
):
    order = await shop_db.orders.find_unique(
        where={"id": order_id},
        include={
            "payments": True,
            "shipping": {
                "include": {
                    "addresses": True,
                }
            },
            "customers": True,
        },
    )

    if not order:
        return Response(status_code=404)

    return order


@router.patch("/{order_id}/cancel")
async def handle_cancel_order(
    order_id: int,
    shop_db: ShopsClient = Depends(get_shops_db),
):
    order = await shop_db.orders.find_unique(where={"id": order_id})

    if not order:
        return Response(status_code=404)

    await shop_db.payments.update(
        where={"id": order.payment_id},
        data={"status": PaymentStatus.CANCELLED},
    )

    await shop_db.shipping.update(
        where={"id": order.shipping_id},
        data={"status": ShippingStatus.CANCELLED},
    )

    return Response(status_code=204)
