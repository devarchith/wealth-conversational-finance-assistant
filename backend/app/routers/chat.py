from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_ai_provider, get_current_user, get_store
from app.models import ChatRequest, ChatResponse
from app.services.rule_engine import EngineResult, RuleBasedEngine


router = APIRouter(prefix="/chat", tags=["chat"])
rule_engine = RuleBasedEngine()


def run_chat(payload: ChatRequest, user: dict, store, engine, engine_name: str) -> ChatResponse:
    if payload.conversation_id:
        conversation = store.get_conversation(user["id"], payload.conversation_id)
        if not conversation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    else:
        conversation = store.create_conversation(user["id"], payload.message)
    store.add_message(user["id"], conversation["id"], {"role": "user", "content": payload.message, "engine": engine_name, "intent": None, "entities": [], "confidence": None})
    result: EngineResult = engine.respond(payload.message)
    store.add_message(user["id"], conversation["id"], {"role": "assistant", "content": result.response, "engine": engine_name, "intent": result.intent, "entities": [e.model_dump() for e in result.entities], "confidence": result.confidence})
    return ChatResponse(response=result.response, intent=result.intent, entities=result.entities, confidence=result.confidence, engine=engine_name, conversation_id=conversation["id"])


@router.post("/rule-based", response_model=ChatResponse)
def rule_based(payload: ChatRequest, user: Annotated[dict, Depends(get_current_user)], store=Depends(get_store)):
    return run_chat(payload, user, store, rule_engine, rule_engine.name)


@router.post("/ai", response_model=ChatResponse)
def ai_chat(payload: ChatRequest, user: Annotated[dict, Depends(get_current_user)], store=Depends(get_store), ai_provider=Depends(get_ai_provider)):
    return run_chat(payload, user, store, ai_provider, ai_provider.name)

