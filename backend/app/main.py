from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import Settings, get_settings
from app.routers import admin, auth, chat, history, profiles, providers, recommendations
from app.services.ai import MockAIProvider, OpenAICompatibleProvider
from app.services.email import MockEmailProvider, SMTPEmailProvider
from app.services.storage import CloudinaryStorageProvider, MockStorageProvider
from app.store import MemoryStore, MongoStore, Store


logger = logging.getLogger(__name__)


def build_providers(settings: Settings):
    fallbacks: list[str] = []
    if settings.ai_provider == "openai" and settings.openai_api_key and settings.openai_model:
        ai_provider = OpenAICompatibleProvider(settings.openai_api_key, settings.openai_base_url, settings.openai_model)
    else:
        ai_provider = MockAIProvider()
        if settings.ai_provider != "mock":
            fallbacks.append("ai")

    if settings.email_provider == "smtp" and all([settings.smtp_host, settings.smtp_username, settings.smtp_password, settings.smtp_from_email]):
        email_provider = SMTPEmailProvider(settings.smtp_host, settings.smtp_port, settings.smtp_username, settings.smtp_password, settings.smtp_from_email)  # type: ignore[arg-type]
    else:
        email_provider = MockEmailProvider()
        if settings.email_provider != "mock":
            fallbacks.append("email")

    if settings.storage_provider == "cloudinary" and all([settings.cloudinary_cloud_name, settings.cloudinary_api_key, settings.cloudinary_api_secret]):
        storage_provider = CloudinaryStorageProvider(settings.cloudinary_cloud_name, settings.cloudinary_api_key, settings.cloudinary_api_secret)  # type: ignore[arg-type]
    else:
        storage_provider = MockStorageProvider()
        if settings.storage_provider != "mock":
            fallbacks.append("storage")
    return ai_provider, email_provider, storage_provider, fallbacks


def create_app(settings: Settings | None = None, store: Store | None = None) -> FastAPI:
    settings = settings or get_settings()
    store = store or MongoStore(settings.mongodb_uri, settings.mongodb_database)
    ai_provider, email_provider, storage_provider, fallbacks = build_providers(settings)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if app.state.store.ping():
            app.state.store.ensure_indexes()
        else:
            logger.warning("MongoDB is unavailable; data routes will fail until it is reachable")
        yield

    app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
    app.state.settings = settings
    app.state.store = store
    app.state.ai_provider = ai_provider
    app.state.email_provider = email_provider
    app.state.storage_provider = storage_provider
    app.state.provider_fallbacks = fallbacks
    app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

    @app.get("/api/health", tags=["health"])
    def health(request: Request):
        return {"status": "ok", "database": "available" if request.app.state.store.ping() else "unavailable", "providers": {"ai": request.app.state.ai_provider.name, "email": request.app.state.email_provider.name, "storage": request.app.state.storage_provider.name}, "fallbacks": request.app.state.provider_fallbacks}

    for router in (auth.router, profiles.router, recommendations.router, chat.router, history.router, providers.router, admin.router):
        app.include_router(router, prefix="/api")
    return app


app = create_app()

