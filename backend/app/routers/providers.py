from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.dependencies import get_current_user, get_storage_provider, get_store


router = APIRouter(tags=["providers"])
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "application/pdf"}


@router.get("/notifications/history")
def notification_history(user: Annotated[dict, Depends(get_current_user)], store=Depends(get_store)):
    return {"items": store.list_notifications(user["id"])}


@router.post("/storage/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(
    user: Annotated[dict, Depends(get_current_user)],
    file: UploadFile = File(...),
    store=Depends(get_store),
    storage_provider=Depends(get_storage_provider),
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Unsupported file type")
    content = await file.read()
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is empty")
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File exceeds 5 MB")
    safe_name = Path(file.filename or "upload").name.replace("\x00", "")[:150]
    uploaded = storage_provider.upload(content, safe_name, file.content_type)
    return store.add_file({"user_id": user["id"], "purpose": "profile_or_supporting_document", "original_name": safe_name, "content_type": file.content_type, "size": len(content), "provider": storage_provider.name, **uploaded})

