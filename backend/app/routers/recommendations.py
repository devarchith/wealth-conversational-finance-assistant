from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_current_user, get_store
from app.models import FinancialProfile, RecommendationSummary
from app.services.recommendations import calculate_recommendations


router = APIRouter(tags=["recommendations"])


@router.get("/recommendations", response_model=RecommendationSummary)
def recommendations(user: Annotated[dict, Depends(get_current_user)], store=Depends(get_store)):
    profile = FinancialProfile.model_validate(store.get_financial_profile(user["id"]) or {})
    return calculate_recommendations(profile)

