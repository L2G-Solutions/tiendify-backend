from fastapi import APIRouter, Depends, HTTPException

from app.core.security import get_current_user, valid_access_token
from app.database import get_client_db
from app.models.auth import UserTokenInfo
from database.client_db import Prisma

router = APIRouter(tags=["auth"])


@router.get(
    "/me",
    summary="Get current user information",
    dependencies=[Depends(valid_access_token)],
)
async def get_logged_user(
    user: UserTokenInfo = Depends(get_current_user),
    client_db: Prisma = Depends(get_client_db),
):
    user_info = await client_db.users.find_unique({"email": user.email})

    if not user_info:
        raise HTTPException(status_code=404, detail="User not found")

    return user_info
