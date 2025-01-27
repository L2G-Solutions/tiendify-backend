import urllib
import urllib.parse

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.config.config import settings
from app.core.security import get_current_user, valid_access_token
from app.database import get_client_db
from app.models.auth import UserTokenInfo
from database.client_db import Prisma

router = APIRouter(tags=["proxy"], dependencies=[Depends(valid_access_token)])


async def shop_reverse_proxy(request: Request, client_db: Prisma, user: UserTokenInfo):
    user_info = await client_db.users.find_first(
        where={"email": user.email},
        include={
            "shop": {
                "include": {
                    "resource_group": True,
                },
            }
        },
    )
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if not user_info.shop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found"
        )

    shop_info = user_info.shop[0]

    if not shop_info.resource_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource group not found"
        )

    body = None
    if request.method in ["POST", "PUT", "DELETE"]:
        try:
            body = await request.json()
        except ValueError:
            body = await request.body()
            if body == b"":
                body = None

    shop_api_url = shop_info.resource_group.api_url

    target_url = urllib.parse.urlunparse(
        (
            urllib.parse.urlparse(shop_api_url).scheme,
            urllib.parse.urlparse(shop_api_url).netloc,
            request.url.path,
            None,
            request.url.query,
            None,
        )
    )

    headers = {"Authorization": f"Bearer {settings.STORE_API_SCRET_KEY}"}

    response = await httpx.AsyncClient().request(
        method=request.method,
        url=target_url,
        json=body,
        headers=headers,
    )
    parsed_response = response.json()

    return JSONResponse(content=parsed_response, status_code=response.status_code)


@router.get("/{path:path}")
async def shop_get_proxy(
    request: Request,
    client_db: Prisma = Depends(get_client_db),
    user=Depends(get_current_user),
):
    return await shop_reverse_proxy(request, client_db, user)


@router.post("/{path:path}")
async def shop_post_proxy(
    request: Request,
    client_db: Prisma = Depends(get_client_db),
    user=Depends(get_current_user),
):
    return await shop_reverse_proxy(request, client_db, user)


@router.put("/{path:path}")
async def shop_put_proxy(
    request: Request,
    client_db: Prisma = Depends(get_client_db),
    user=Depends(get_current_user),
):
    return await shop_reverse_proxy(request, client_db, user)


@router.delete("/{path:path}")
async def shop_delete_proxy(
    request: Request,
    client_db: Prisma = Depends(get_client_db),
    user=Depends(get_current_user),
):
    return await shop_reverse_proxy(request, client_db, user)
