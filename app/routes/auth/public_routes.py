from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import RedirectResponse, JSONResponse
from app.config.config import settings
from app.core.security import keycloak_openid

router = APIRouter()


@router.get("/login", summary="Redirect to Keycloak login page", tags=["auth"])
async def redirect_to_keycloak():
    authorization_url = (
        f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/auth"
        f"?client_id={settings.KEYCLOAK_CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={settings.REDIRECT_URI}"
    )
    return RedirectResponse(url=authorization_url)


@router.get("/callback", tags=["auth"])
async def auth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Authorization code missing"
        )

    token_response = keycloak_openid.token(
        grant_type="authorization_code",
        code=code,
        redirect_uri=settings.REDIRECT_URI,
    )

    return JSONResponse(content=token_response)
