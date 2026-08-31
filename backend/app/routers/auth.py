from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.dependencies import get_current_user, get_email_provider, get_store
from app.models import LoginRequest, PasswordResetConfirm, PasswordResetRequest, RegisterRequest, TokenResponse, UserPublic
from app.security import create_access_token, hash_password, hash_token, make_reset_token, verify_password


router = APIRouter(prefix="/auth", tags=["authentication"])


def public_user(user: dict) -> UserPublic:
    return UserPublic.model_validate({k: user[k] for k in ("id", "email", "role", "is_active", "created_at")})


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, request: Request, store=Depends(get_store), email_provider=Depends(get_email_provider)):
    try:
        user = store.create_user(str(payload.email), hash_password(payload.password))
    except ValueError as exc:
        if str(exc) == "duplicate_email":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="An account with this email already exists") from None
        raise
    message_id = email_provider.send(user["email"], "Welcome to Wealth Assistant", "Your account has been created. Never share your password or financial-service credentials.")
    store.add_notification({"user_id": user["id"], "kind": "registration", "recipient": user["email"], "provider": email_provider.name, "status": "sent", "provider_message_id": message_id})
    token = create_access_token(user["id"], user["role"], request.app.state.settings.secret_key, request.app.state.settings.access_token_expire_minutes)
    return TokenResponse(access_token=token, user=public_user(user))


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, request: Request, store=Depends(get_store)):
    user = store.get_user_by_email(str(payload.email))
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    token = create_access_token(user["id"], user["role"], request.app.state.settings.secret_key, request.app.state.settings.access_token_expire_minutes)
    return TokenResponse(access_token=token, user=public_user(user))


@router.get("/me", response_model=UserPublic)
def me(user: Annotated[dict, Depends(get_current_user)]):
    return public_user(user)


@router.post("/logout")
def logout(_: Annotated[dict, Depends(get_current_user)]):
    return {"message": "Token logout is client-side; discard the access token"}


@router.post("/password-reset/request")
def request_password_reset(payload: PasswordResetRequest, request: Request, store=Depends(get_store), email_provider=Depends(get_email_provider)):
    user = store.get_user_by_email(str(payload.email))
    if user:
        raw_token, token_hash = make_reset_token()
        store.save_reset_token(user["id"], token_hash, datetime.now(UTC) + timedelta(hours=1))
        reset_url = f"{request.app.state.settings.frontend_url.rstrip('/')}/reset-password?token={raw_token}"
        message_id = email_provider.send(user["email"], "Reset your Wealth Assistant password", f"Use this one-time link within one hour: {reset_url}")
        store.add_notification({"user_id": user["id"], "kind": "password_reset", "recipient": user["email"], "provider": email_provider.name, "status": "sent", "provider_message_id": message_id})
    return {"message": "If the account exists, a reset message has been sent"}


@router.post("/password-reset/confirm")
def confirm_password_reset(payload: PasswordResetConfirm, store=Depends(get_store)):
    token = store.consume_reset_token(hash_token(payload.token), datetime.now(UTC))
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired reset token")
    register_model = RegisterRequest(email="reset-validation@example.com", password=payload.new_password)
    store.update_user_password(token["user_id"], hash_password(register_model.password))
    return {"message": "Password reset successful"}
