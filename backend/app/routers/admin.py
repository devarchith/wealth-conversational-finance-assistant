from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.dependencies import get_store, require_admin


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/summary")
def summary(request: Request, _: Annotated[dict, Depends(require_admin)], store=Depends(get_store)):
    return {
        "counts": store.counts(),
        "database_available": store.ping(),
        "providers": {
            "ai": request.app.state.ai_provider.name,
            "email": request.app.state.email_provider.name,
            "storage": request.app.state.storage_provider.name,
        },
        "fallbacks": request.app.state.provider_fallbacks,
    }

