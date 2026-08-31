from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends

from app.dependencies import get_current_user, get_store
from app.models import FinancialProfile, UserProfile


router = APIRouter(tags=["profiles"])


@router.get("/profile", response_model=UserProfile)
def get_profile(user: Annotated[dict, Depends(get_current_user)], store=Depends(get_store)):
    return UserProfile.model_validate(store.get_profile(user["id"]) or {})


@router.put("/profile", response_model=UserProfile)
def update_profile(payload: UserProfile, user: Annotated[dict, Depends(get_current_user)], store=Depends(get_store)):
    return UserProfile.model_validate(store.save_profile(user["id"], payload.model_dump()))


@router.get("/financial-profile", response_model=FinancialProfile)
def get_financial_profile(user: Annotated[dict, Depends(get_current_user)], store=Depends(get_store)):
    return FinancialProfile.model_validate(store.get_financial_profile(user["id"]) or {})


@router.put("/financial-profile", response_model=FinancialProfile)
def update_financial_profile(payload: FinancialProfile, user: Annotated[dict, Depends(get_current_user)], store=Depends(get_store)):
    data = payload.model_dump(mode="json")
    for goal in data["goals"]:
        goal["id"] = goal.get("id") or uuid4().hex
    return FinancialProfile.model_validate(store.save_financial_profile(user["id"], data))

