from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.models import Role
from app.security import decode_access_token


bearer = HTTPBearer(auto_error=False)


def get_store(request: Request):
    return request.app.state.store


def get_email_provider(request: Request):
    return request.app.state.email_provider


def get_storage_provider(request: Request):
    return request.app.state.storage_provider


def get_ai_provider(request: Request):
    return request.app.state.ai_provider


def get_current_user(
    request: Request,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
) -> dict:
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    try:
        payload = decode_access_token(credentials.credentials, request.app.state.settings.secret_key)
        if payload.get("type") != "access":
            raise ValueError("invalid token type")
    except (jwt.PyJWTError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token") from None
    user = request.app.state.store.get_user(payload["sub"])
    if not user or not user.get("is_active"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or inactive user")
    return user


def require_admin(user: Annotated[dict, Depends(get_current_user)]) -> dict:
    if user.get("role") != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Administrator access required")
    return user

