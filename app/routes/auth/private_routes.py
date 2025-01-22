from fastapi import APIRouter, Depends

from app.core.security import get_current_user, valid_access_token

router = APIRouter(tags=["auth"])


@router.get(
    "/me",
    summary="Get current user information",
    dependencies=[Depends(valid_access_token)],
)
async def get_logged_user(user: dict = Depends(get_current_user)):
    return {"user": user}
