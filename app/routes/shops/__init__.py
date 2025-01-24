from fastapi import APIRouter, HTTPException, Depends, status
from app.database import get_client_db
from app.models.shop import ShopCreate
from database.client_db import Prisma
from prisma.errors import PrismaError

router = APIRouter()


@router.post("/", tags=["shops"])
async def create_shop(shop: ShopCreate, client_db: Prisma = Depends(get_client_db)):
    try:
        user = await client_db.users.find_unique(where={"id": str(shop.owner_id)})

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid data"
            )

        if shop.resource_group_id:
            resource_group = await client_db.resource_group.find_unique(
                where={"id": str(shop.resource_group_id)}
            )

            if not resource_group:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid data"
                )

        shop_data = {
            "name": shop.name,
            "headline": shop.headline,
            "about": shop.about,
            "currency": shop.currency,
            "logoimg": shop.logoimg,
            "bannerimg": shop.bannerimg,
            "country": shop.country,
            "status": shop.status,
            "verified": shop.verified,
            "owner_id": str(shop.owner_id),
        }

        if shop.resource_group_id:
            shop_data["resource_group_id"] = str(shop.resource_group_id)

        new_shop = await client_db.shop.create(data=shop_data)
        return new_shop

    except PrismaError as e:
        if "P2003" in str(e):
            if "shop_owner_id_fkey" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="OI"
                )
            elif "resource_group_id_fkey" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="RI"
                )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
