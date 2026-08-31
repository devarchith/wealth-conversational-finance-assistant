from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
from threading import RLock
from typing import Any, Protocol
from uuid import uuid4

from pymongo import ASCENDING, DESCENDING, MongoClient
from pymongo.database import Database


def utcnow() -> datetime:
    return datetime.now(UTC)


def new_id() -> str:
    return uuid4().hex


class Store(Protocol):
    def ensure_indexes(self) -> None: ...
    def ping(self) -> bool: ...
    def create_user(self, email: str, password_hash: str, role: str = "user") -> dict: ...
    def get_user_by_email(self, email: str) -> dict | None: ...
    def get_user(self, user_id: str) -> dict | None: ...
    def update_user_password(self, user_id: str, password_hash: str) -> None: ...
    def get_profile(self, user_id: str) -> dict | None: ...
    def save_profile(self, user_id: str, data: dict) -> dict: ...
    def get_financial_profile(self, user_id: str) -> dict | None: ...
    def save_financial_profile(self, user_id: str, data: dict) -> dict: ...
    def save_reset_token(self, user_id: str, token_hash: str, expires_at: datetime) -> dict: ...
    def consume_reset_token(self, token_hash: str, now: datetime) -> dict | None: ...
    def create_conversation(self, user_id: str, title: str) -> dict: ...
    def get_conversation(self, user_id: str, conversation_id: str) -> dict | None: ...
    def add_message(self, user_id: str, conversation_id: str, data: dict) -> dict: ...
    def list_conversations(self, user_id: str, page: int, page_size: int) -> tuple[list[dict], int]: ...
    def list_messages(self, user_id: str, conversation_id: str) -> list[dict]: ...
    def delete_conversation(self, user_id: str, conversation_id: str) -> bool: ...
    def add_notification(self, data: dict) -> dict: ...
    def list_notifications(self, user_id: str) -> list[dict]: ...
    def add_file(self, data: dict) -> dict: ...
    def counts(self) -> dict[str, int]: ...


class MemoryStore:
    """Thread-safe repository used by tests and explicit local demo mode."""

    def __init__(self) -> None:
        self._lock = RLock()
        self.users: dict[str, dict] = {}
        self.profiles: dict[str, dict] = {}
        self.financial_profiles: dict[str, dict] = {}
        self.reset_tokens: dict[str, dict] = {}
        self.conversations: dict[str, dict] = {}
        self.messages: dict[str, dict] = {}
        self.notifications: dict[str, dict] = {}
        self.files: dict[str, dict] = {}

    def ensure_indexes(self) -> None:
        return None

    def ping(self) -> bool:
        return True

    def create_user(self, email: str, password_hash: str, role: str = "user") -> dict:
        with self._lock:
            email = email.lower().strip()
            if self.get_user_by_email(email):
                raise ValueError("duplicate_email")
            now = utcnow()
            item = {"id": new_id(), "email": email, "password_hash": password_hash, "role": role, "is_active": True, "created_at": now, "updated_at": now}
            self.users[item["id"]] = item
            return deepcopy(item)

    def get_user_by_email(self, email: str) -> dict | None:
        email = email.lower().strip()
        return next((deepcopy(v) for v in self.users.values() if v["email"] == email), None)

    def get_user(self, user_id: str) -> dict | None:
        item = self.users.get(user_id)
        return deepcopy(item) if item else None

    def update_user_password(self, user_id: str, password_hash: str) -> None:
        with self._lock:
            self.users[user_id]["password_hash"] = password_hash
            self.users[user_id]["updated_at"] = utcnow()

    def get_profile(self, user_id: str) -> dict | None:
        item = self.profiles.get(user_id)
        return deepcopy(item) if item else None

    def save_profile(self, user_id: str, data: dict) -> dict:
        with self._lock:
            item = {**deepcopy(data), "user_id": user_id, "updated_at": utcnow()}
            self.profiles[user_id] = item
            return deepcopy(item)

    def get_financial_profile(self, user_id: str) -> dict | None:
        item = self.financial_profiles.get(user_id)
        return deepcopy(item) if item else None

    def save_financial_profile(self, user_id: str, data: dict) -> dict:
        with self._lock:
            item = {**deepcopy(data), "user_id": user_id, "updated_at": utcnow()}
            self.financial_profiles[user_id] = item
            return deepcopy(item)

    def save_reset_token(self, user_id: str, token_hash: str, expires_at: datetime) -> dict:
        with self._lock:
            item = {"id": new_id(), "user_id": user_id, "token_hash": token_hash, "expires_at": expires_at, "used_at": None, "created_at": utcnow()}
            self.reset_tokens[token_hash] = item
            return deepcopy(item)

    def consume_reset_token(self, token_hash: str, now: datetime) -> dict | None:
        with self._lock:
            item = self.reset_tokens.get(token_hash)
            if not item or item["used_at"] or item["expires_at"] <= now:
                return None
            item["used_at"] = now
            return deepcopy(item)

    def create_conversation(self, user_id: str, title: str) -> dict:
        with self._lock:
            now = utcnow()
            item = {"id": new_id(), "user_id": user_id, "title": title[:80], "created_at": now, "updated_at": now, "last_engine": None, "last_intent": None}
            self.conversations[item["id"]] = item
            return deepcopy(item)

    def get_conversation(self, user_id: str, conversation_id: str) -> dict | None:
        item = self.conversations.get(conversation_id)
        return deepcopy(item) if item and item["user_id"] == user_id else None

    def add_message(self, user_id: str, conversation_id: str, data: dict) -> dict:
        with self._lock:
            if not self.get_conversation(user_id, conversation_id):
                raise KeyError("conversation_not_found")
            item = {**deepcopy(data), "id": new_id(), "user_id": user_id, "conversation_id": conversation_id, "created_at": utcnow()}
            self.messages[item["id"]] = item
            convo = self.conversations[conversation_id]
            convo["updated_at"] = item["created_at"]
            if item.get("role") == "assistant":
                convo["last_engine"] = item.get("engine")
                convo["last_intent"] = item.get("intent")
            return deepcopy(item)

    def list_conversations(self, user_id: str, page: int, page_size: int) -> tuple[list[dict], int]:
        rows = [deepcopy(v) for v in self.conversations.values() if v["user_id"] == user_id]
        rows.sort(key=lambda x: x["updated_at"], reverse=True)
        total = len(rows)
        start = (page - 1) * page_size
        return rows[start:start + page_size], total

    def list_messages(self, user_id: str, conversation_id: str) -> list[dict]:
        if not self.get_conversation(user_id, conversation_id):
            raise KeyError("conversation_not_found")
        rows = [deepcopy(v) for v in self.messages.values() if v["user_id"] == user_id and v["conversation_id"] == conversation_id]
        rows.sort(key=lambda x: x["created_at"])
        return rows

    def delete_conversation(self, user_id: str, conversation_id: str) -> bool:
        with self._lock:
            if not self.get_conversation(user_id, conversation_id):
                return False
            del self.conversations[conversation_id]
            for message_id in [k for k, v in self.messages.items() if v["user_id"] == user_id and v["conversation_id"] == conversation_id]:
                del self.messages[message_id]
            return True

    def add_notification(self, data: dict) -> dict:
        with self._lock:
            item = {**deepcopy(data), "id": new_id(), "created_at": utcnow()}
            self.notifications[item["id"]] = item
            return deepcopy(item)

    def list_notifications(self, user_id: str) -> list[dict]:
        rows = [deepcopy(v) for v in self.notifications.values() if v.get("user_id") == user_id]
        return sorted(rows, key=lambda x: x["created_at"], reverse=True)

    def add_file(self, data: dict) -> dict:
        with self._lock:
            item = {**deepcopy(data), "id": new_id(), "created_at": utcnow()}
            self.files[item["id"]] = item
            return deepcopy(item)

    def counts(self) -> dict[str, int]:
        return {"users": len(self.users), "conversations": len(self.conversations), "messages": len(self.messages), "files": len(self.files)}


class MongoStore:
    def __init__(self, uri: str, database: str) -> None:
        self.client = MongoClient(uri, serverSelectionTimeoutMS=1500, tz_aware=True)
        self.db: Database = self.client[database]

    @staticmethod
    def _clean(item: dict | None) -> dict | None:
        if not item:
            return None
        item = dict(item)
        item.pop("_id", None)
        return item

    def ensure_indexes(self) -> None:
        self.db.users.create_index("email", unique=True)
        self.db.user_profiles.create_index("user_id", unique=True)
        self.db.financial_profiles.create_index("user_id", unique=True)
        self.db.password_reset_tokens.create_index("token_hash", unique=True)
        self.db.password_reset_tokens.create_index("expires_at", expireAfterSeconds=0)
        self.db.conversations.create_index([("user_id", ASCENDING), ("updated_at", DESCENDING)])
        self.db.messages.create_index([("user_id", ASCENDING), ("conversation_id", ASCENDING), ("created_at", ASCENDING)])

    def ping(self) -> bool:
        try:
            self.client.admin.command("ping")
            return True
        except Exception:
            return False

    def create_user(self, email: str, password_hash: str, role: str = "user") -> dict:
        now = utcnow()
        item = {"id": new_id(), "email": email.lower().strip(), "password_hash": password_hash, "role": role, "is_active": True, "created_at": now, "updated_at": now}
        try:
            self.db.users.insert_one(item)
        except Exception as exc:
            if "duplicate" in str(exc).lower() or "E11000" in str(exc):
                raise ValueError("duplicate_email") from exc
            raise
        return self._clean(item)  # type: ignore[return-value]

    def get_user_by_email(self, email: str) -> dict | None:
        return self._clean(self.db.users.find_one({"email": email.lower().strip()}))

    def get_user(self, user_id: str) -> dict | None:
        return self._clean(self.db.users.find_one({"id": user_id}))

    def update_user_password(self, user_id: str, password_hash: str) -> None:
        self.db.users.update_one({"id": user_id}, {"$set": {"password_hash": password_hash, "updated_at": utcnow()}})

    def get_profile(self, user_id: str) -> dict | None:
        return self._clean(self.db.user_profiles.find_one({"user_id": user_id}))

    def save_profile(self, user_id: str, data: dict) -> dict:
        item = {**data, "user_id": user_id, "updated_at": utcnow()}
        self.db.user_profiles.update_one({"user_id": user_id}, {"$set": item}, upsert=True)
        return item

    def get_financial_profile(self, user_id: str) -> dict | None:
        return self._clean(self.db.financial_profiles.find_one({"user_id": user_id}))

    def save_financial_profile(self, user_id: str, data: dict) -> dict:
        item = {**data, "user_id": user_id, "updated_at": utcnow()}
        self.db.financial_profiles.update_one({"user_id": user_id}, {"$set": item}, upsert=True)
        return item

    def save_reset_token(self, user_id: str, token_hash: str, expires_at: datetime) -> dict:
        item = {"id": new_id(), "user_id": user_id, "token_hash": token_hash, "expires_at": expires_at, "used_at": None, "created_at": utcnow()}
        self.db.password_reset_tokens.insert_one(item)
        return self._clean(item)  # type: ignore[return-value]

    def consume_reset_token(self, token_hash: str, now: datetime) -> dict | None:
        return self._clean(self.db.password_reset_tokens.find_one_and_update(
            {"token_hash": token_hash, "used_at": None, "expires_at": {"$gt": now}},
            {"$set": {"used_at": now}},
        ))

    def create_conversation(self, user_id: str, title: str) -> dict:
        now = utcnow()
        item = {"id": new_id(), "user_id": user_id, "title": title[:80], "created_at": now, "updated_at": now, "last_engine": None, "last_intent": None}
        self.db.conversations.insert_one(item)
        return self._clean(item)  # type: ignore[return-value]

    def get_conversation(self, user_id: str, conversation_id: str) -> dict | None:
        return self._clean(self.db.conversations.find_one({"id": conversation_id, "user_id": user_id}))

    def add_message(self, user_id: str, conversation_id: str, data: dict) -> dict:
        if not self.get_conversation(user_id, conversation_id):
            raise KeyError("conversation_not_found")
        item = {**data, "id": new_id(), "user_id": user_id, "conversation_id": conversation_id, "created_at": utcnow()}
        self.db.messages.insert_one(item)
        update: dict[str, Any] = {"updated_at": item["created_at"]}
        if item.get("role") == "assistant":
            update |= {"last_engine": item.get("engine"), "last_intent": item.get("intent")}
        self.db.conversations.update_one({"id": conversation_id, "user_id": user_id}, {"$set": update})
        return self._clean(item)  # type: ignore[return-value]

    def list_conversations(self, user_id: str, page: int, page_size: int) -> tuple[list[dict], int]:
        query = {"user_id": user_id}
        cursor = self.db.conversations.find(query, {"_id": 0}).sort("updated_at", DESCENDING).skip((page - 1) * page_size).limit(page_size)
        return list(cursor), self.db.conversations.count_documents(query)

    def list_messages(self, user_id: str, conversation_id: str) -> list[dict]:
        if not self.get_conversation(user_id, conversation_id):
            raise KeyError("conversation_not_found")
        return list(self.db.messages.find({"user_id": user_id, "conversation_id": conversation_id}, {"_id": 0}).sort("created_at", ASCENDING))

    def delete_conversation(self, user_id: str, conversation_id: str) -> bool:
        result = self.db.conversations.delete_one({"id": conversation_id, "user_id": user_id})
        if not result.deleted_count:
            return False
        self.db.messages.delete_many({"conversation_id": conversation_id, "user_id": user_id})
        return True

    def add_notification(self, data: dict) -> dict:
        item = {**data, "id": new_id(), "created_at": utcnow()}
        self.db.notification_events.insert_one(item)
        return self._clean(item)  # type: ignore[return-value]

    def list_notifications(self, user_id: str) -> list[dict]:
        return list(self.db.notification_events.find({"user_id": user_id}, {"_id": 0}).sort("created_at", DESCENDING).limit(100))

    def add_file(self, data: dict) -> dict:
        item = {**data, "id": new_id(), "created_at": utcnow()}
        self.db.stored_files.insert_one(item)
        return self._clean(item)  # type: ignore[return-value]

    def counts(self) -> dict[str, int]:
        return {"users": self.db.users.count_documents({}), "conversations": self.db.conversations.count_documents({}), "messages": self.db.messages.count_documents({}), "files": self.db.stored_files.count_documents({})}

