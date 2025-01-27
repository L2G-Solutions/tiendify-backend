from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse, RedirectResponse

from app.config.config import settings
from app.core.security import keycloak_openid

router = APIRouter()


@router.get("/login", summary="Redirect to Keycloak login page", tags=["auth"])
async def redirect_to_keycloak(
    request: Request, redirect_uri: str = None, next: str = None
):
    if not redirect_uri:
        host = request.headers["host"]
        redirect_uri = f"https://{host}/authorize"

    if next:
        redirect_uri += f"?next={next}"

    authorization_url = (
        f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/auth"
        f"?client_id={settings.KEYCLOAK_CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={redirect_uri}"
    )
    return RedirectResponse(url=authorization_url)


@router.post(
    "/authorize",
    summary="Takes the authorization code and set the access token",
    tags=["auth"],
)
async def authorize(
    request: Request, code: str = None, validation_uri: str = None, next: str = None
):
    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Authorization code missing"
        )

    if not validation_uri:
        host = request.headers["host"]
        validation_uri = f"https://{host}/authorize"

    if next:
        validation_uri += f"?next={next}"

    try:
        token_response = keycloak_openid.token(
            grant_type="authorization_code", code=code, redirect_uri=validation_uri
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    response = JSONResponse(content=token_response)

    response.set_cookie(
        key="access_token",
        value=token_response["access_token"],
        httponly=True,
        samesite="lax",
        domain="localhost",
        expires=datetime.now(timezone.utc)
        + timedelta(seconds=token_response["expires_in"]),
        max_age=token_response["expires_in"],
    )

    response.set_cookie(
        key="refresh_token",
        value=token_response["refresh_token"],
        httponly=True,
        samesite="lax",
        domain="localhost",
        expires=datetime.now(timezone.utc)
        + timedelta(seconds=token_response["refresh_expires_in"]),
        max_age=token_response["refresh_expires_in"],
    )

    return response
