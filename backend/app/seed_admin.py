"""Create an initial admin without embedding credentials in source control."""

import argparse
import getpass

from app.config import get_settings
from app.security import hash_password
from app.store import MongoStore


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", required=True)
    args = parser.parse_args()
    password = getpass.getpass("Admin password: ")
    if len(password) < 10 or not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
        raise SystemExit("Password must be at least 10 characters and contain a letter and number")
    settings = get_settings()
    store = MongoStore(settings.mongodb_uri, settings.mongodb_database)
    store.ensure_indexes()
    store.create_user(args.email, hash_password(password), role="admin")
    print("Admin created")


if __name__ == "__main__":
    main()

