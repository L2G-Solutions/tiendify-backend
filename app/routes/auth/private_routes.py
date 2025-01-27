from fastapi import APIRouter, Depends, HTTPException, Request, Response

from app.core.security import get_current_user, keycloak_openid, valid_access_token
from app.database import get_client_db
from app.models.auth import UserTokenInfo
from database.client_db import Prisma

router = APIRouter(tags=["auth"], dependencies=[Depends(valid_access_token)])


@router.get(
    "/me",
    summary="Get current user information",
)
async def get_logged_user(
    user: UserTokenInfo = Depends(get_current_user),
    client_db: Prisma = Depends(get_client_db),
):
    user_info = await client_db.users.find_unique(
        {"email": user.email}, include={"shop": True}
    )

    if not user_info:
        raise HTTPException(status_code=404, detail="User not found")

    return user_info


@router.post("/logout", summary="Logout user")
async def logout(
    request: Request,
    response: Response,
):
    refresh_token = request.cookies.get("refresh_token")

    try:
        keycloak_openid.logout(refresh_token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return {"message": "User logged out"}
