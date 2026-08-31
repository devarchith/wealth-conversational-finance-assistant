from abc import ABC, abstractmethod
import hashlib

import cloudinary
import cloudinary.uploader


class StorageProvider(ABC):
    name: str

    @abstractmethod
    def upload(self, content: bytes, filename: str, content_type: str) -> dict: ...


class MockStorageProvider(StorageProvider):
    name = "mock"

    def upload(self, content: bytes, filename: str, content_type: str) -> dict:
        digest = hashlib.sha256(content).hexdigest()[:20]
        return {"public_id": f"mock/{digest}", "secure_url": f"mock://storage/{digest}/{filename}", "content_type": content_type}


class CloudinaryStorageProvider(StorageProvider):
    name = "cloudinary"

    def __init__(self, cloud_name: str, api_key: str, api_secret: str) -> None:
        cloudinary.config(cloud_name=cloud_name, api_key=api_key, api_secret=api_secret, secure=True)

    def upload(self, content: bytes, filename: str, content_type: str) -> dict:
        result = cloudinary.uploader.upload(content, folder="wealth-assistant", filename_override=filename, resource_type="auto", use_filename=True, unique_filename=True)
        return {"public_id": result["public_id"], "secure_url": result["secure_url"], "content_type": content_type}

