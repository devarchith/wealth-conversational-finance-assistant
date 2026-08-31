from datetime import UTC, datetime, timedelta

import mongomock

from app.store import MongoStore


def test_mongo_store_persistence_and_ownership_contract():
    store = MongoStore("mongodb://unused", "test", client=mongomock.MongoClient(tz_aware=True))
    store.ensure_indexes()
    one = store.create_user("one@example.com", "hash-one")
    two = store.create_user("two@example.com", "hash-two")
    assert store.ping()
    store.save_profile(one["id"], {"display_name": "One"})
    store.save_financial_profile(one["id"], {"monthly_income": 1000})
    assert store.get_profile(one["id"])["display_name"] == "One"
    assert store.get_financial_profile(two["id"]) is None

    conversation = store.create_conversation(one["id"], "Private budget")
    store.add_message(one["id"], conversation["id"], {"role": "user", "content": "budget"})
    assert store.get_conversation(two["id"], conversation["id"]) is None
    assert store.list_messages(one["id"], conversation["id"])[0]["content"] == "budget"
    assert not store.delete_conversation(two["id"], conversation["id"])
    assert store.delete_conversation(one["id"], conversation["id"])

    token = store.save_reset_token(one["id"], "token-hash", datetime.now(UTC) + timedelta(minutes=5))
    assert store.consume_reset_token(token["token_hash"], datetime.now(UTC))["user_id"] == one["id"]
    assert store.consume_reset_token(token["token_hash"], datetime.now(UTC)) is None

    counts = store.counts()
    assert counts["users"] == 2
    assert counts["conversations"] == 0


def test_mongo_store_rejects_duplicate_normalized_email():
    store = MongoStore("mongodb://unused", "test", client=mongomock.MongoClient())
    store.ensure_indexes()
    store.create_user("user@example.com", "hash")
    try:
        store.create_user("USER@example.com", "hash")
    except ValueError as exc:
        assert str(exc) == "duplicate_email"
    else:
        raise AssertionError("duplicate email was accepted")
