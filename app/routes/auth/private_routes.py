from fastapi import APIRouter, Depends
from app.core.security import valid_access_token, has_role

router = APIRouter()

@router.get("/private", dependencies=[Depends(valid_access_token)], tags=["auth"])
async def get_private():
    return {"message": "Private endpoint"}

@router.get("/admin", dependencies=[Depends(has_role("admin"))], tags=["auth"])
def get_admin():
    return {"message": "Admin only"}