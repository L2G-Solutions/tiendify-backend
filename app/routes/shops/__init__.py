from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user
from app.database import get_client_db
from app.models.auth import UserTokenInfo
from app.models.shop import ShopCreate
from database.client_db import Prisma
from app.core.tasks import run_in_background
from app.core.cloud_provisioning import create_cloud_resources_for_user_task

router = APIRouter()


@router.post("/", tags=["shops"])
async def create_shop(
    shop: ShopCreate,
    db: Prisma = Depends(get_client_db),
    current_user: UserTokenInfo = Depends(get_current_user),
):
    user = await db.users.find_unique(
        where={"email": current_user.email}, include={"shop": True}
    )

    if user.shop:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already has a shop"
        )

    new_shop = await db.shop.create(
        data={
            "name": shop.name,
            "headline": shop.headline,
            "about": shop.about,
            "currency": shop.currency,
            "country": shop.country,
            "owner_id": user.id,
            "status": "ACTIVE",
            "verified": False,
        }
    )

    run_in_background(
        create_cloud_resources_for_user_task,
        new_shop.id,
    )

    return new_shop


@router.get("/resources", tags=["shops"])
async def handle_get_shop_resources(
    user: UserTokenInfo = Depends(get_current_user), db: Prisma = Depends(get_client_db)
):
    rg = await db.users.find_unique(
        where={"email": user.email},
        include={"shop": {"include": {"resource_group": True}}},
    )

    try:
        if rg.shop[0].resource_group is None:
            raise HTTPException(status_code=404, detail="Shop has no cloud resources")

        return {
            "apiUrl": rg.shop[0].resource_group.api_url,
            "database": bool(rg.shop[0].resource_group.database_id),
            "api": bool(rg.shop[0].resource_group.web_app_id),
            "storage": bool(rg.shop[0].resource_group.azure_blob_storage_id),
        }
    except IndexError:
        raise HTTPException(status_code=404, detail="User has no shop")
