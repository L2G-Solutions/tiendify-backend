from fastapi import APIRouter, Depends
from app.core.security import valid_access_token, has_role

router = APIRouter()

@router.get("/private", dependencies=[Depends(valid_access_token)])
async def get_private():
    return {"message": "Private endpoint"}

@router.get("/admin", dependencies=[Depends(has_role("admin"))])
def get_private():
    return {"message": "Admin only"}