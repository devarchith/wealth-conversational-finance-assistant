from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import get_current_user, get_store
from app.models import Page


router = APIRouter(prefix="/history", tags=["history"])


@router.get("", response_model=Page)
def list_history(user: Annotated[dict, Depends(get_current_user)], page: int = Query(default=1, ge=1), page_size: int = Query(default=20, ge=1, le=100), store=Depends(get_store)):
    rows, total = store.list_conversations(user["id"], page, page_size)
    return Page(items=rows, page=page, page_size=page_size, total=total)


@router.get("/{conversation_id}")
def get_history(conversation_id: str, user: Annotated[dict, Depends(get_current_user)], store=Depends(get_store)):
    conversation = store.get_conversation(user["id"], conversation_id)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    return {"conversation": conversation, "messages": store.list_messages(user["id"], conversation_id)}


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_history(conversation_id: str, user: Annotated[dict, Depends(get_current_user)], store=Depends(get_store)):
    if not store.delete_conversation(user["id"], conversation_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    return None

