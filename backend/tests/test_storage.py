import asyncio

import pytest

import app.services.storage as storage


class FakeUploader:
    calls = []
    upload_result = {
        "secure_url": "https://res.cloudinary.com/demo/image/upload/lamaris/properties/7/photo",
        "public_id": "lamaris/properties/7/photo",
    }
    destroy_result = {"result": "ok"}

    @classmethod
    def upload(cls, *args, **kwargs):
        cls.calls.append(("upload", args, kwargs))
        return cls.upload_result

    @classmethod
    def destroy(cls, *args, **kwargs):
        cls.calls.append(("destroy", args, kwargs))
        return cls.destroy_result


@pytest.fixture()
def cloudinary_settings(monkeypatch):
    monkeypatch.setattr(storage.settings, "cloudinary_cloud_name", "demo")
    monkeypatch.setattr(storage.settings, "cloudinary_api_key", "api-key")
    monkeypatch.setattr(storage.settings, "cloudinary_api_secret", "api-secret")
    FakeUploader.calls = []
    FakeUploader.upload_result = {
        "secure_url": "https://res.cloudinary.com/demo/image/upload/lamaris/properties/7/photo",
        "public_id": "lamaris/properties/7/photo",
    }
    FakeUploader.destroy_result = {"result": "ok"}
    monkeypatch.setattr(storage, "uploader", FakeUploader)
    monkeypatch.setattr(storage.cloudinary, "config", lambda **kwargs: None)
    return storage.settings


def test_cloudinary_upload_returns_secure_url_and_public_id(cloudinary_settings):
    url, public_id = asyncio.run(
        storage.upload_image("lamaris/properties/7/photo", b"jpeg", "image/jpeg")
    )
    assert url.startswith("https://res.cloudinary.com/")
    assert public_id == "lamaris/properties/7/photo"
    method, args, kwargs = FakeUploader.calls[0]
    assert method == "upload"
    assert kwargs["public_id"] == "lamaris/properties/7/photo"
    assert kwargs["asset_folder"] == "lamaris/properties/7"
    assert kwargs["resource_type"] == "image"
    assert kwargs["overwrite"] is False


def test_cloudinary_delete_uses_public_id_and_invalidation(cloudinary_settings):
    asyncio.run(storage.delete_image("lamaris/properties/7/photo"))
    method, args, kwargs = FakeUploader.calls[0]
    assert method == "destroy"
    assert args[0] == "lamaris/properties/7/photo"
    assert kwargs["resource_type"] == "image"
    assert kwargs["type"] == "upload"
    assert kwargs["invalidate"] is True


def test_cloudinary_rejects_path_traversal(cloudinary_settings):
    with pytest.raises(storage.StorageError, match="Invalid Cloudinary public ID"):
        asyncio.run(storage.delete_image("lamaris/properties/../secret"))
    assert FakeUploader.calls == []


def test_cloudinary_rejects_non_lamaris_public_id(cloudinary_settings):
    with pytest.raises(storage.StorageError, match="Invalid Cloudinary public ID"):
        asyncio.run(storage.delete_image("other/properties/7/photo"))
    assert FakeUploader.calls == []


def test_cloudinary_upload_failure_raises_storage_error(cloudinary_settings):
    def fail_upload(*args, **kwargs):
        raise RuntimeError("network failure")

    FakeUploader.upload = fail_upload
    with pytest.raises(storage.StorageError, match="Cloudinary upload failed"):
        asyncio.run(storage.upload_image("lamaris/properties/7/photo", b"jpeg", "image/jpeg"))


def test_cloudinary_delete_failure_raises_storage_error(cloudinary_settings):
    FakeUploader.destroy_result = {"result": "error"}
    with pytest.raises(storage.StorageError, match="Cloudinary delete failed"):
        asyncio.run(storage.delete_image("lamaris/properties/7/photo"))
