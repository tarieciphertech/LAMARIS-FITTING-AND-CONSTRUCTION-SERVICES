import pytest

import app.services.storage as storage


class FakeResponse:
    def __init__(self, status_code):
        self.status_code = status_code


class FakeClient:
    response = FakeResponse(200)
    calls = []

    def __init__(self, *args, **kwargs):
        self.timeout = kwargs.get("timeout")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def post(self, url, **kwargs):
        self.__class__.calls.append(("POST", url, kwargs))
        return self.__class__.response

    async def delete(self, url, **kwargs):
        self.__class__.calls.append(("DELETE", url, kwargs))
        return self.__class__.response


@pytest.fixture()
def supabase_settings(monkeypatch):
    monkeypatch.setattr(storage.settings, "supabase_url", "https://example.supabase.co")
    monkeypatch.setattr(storage.settings, "supabase_service_role_key", "server-secret")
    monkeypatch.setattr(storage.settings, "supabase_storage_bucket", "property-images")
    FakeClient.calls = []
    monkeypatch.setattr(storage.httpx, "AsyncClient", FakeClient)
    return storage.settings


@pytest.mark.asyncio
async def test_supabase_upload_uses_object_endpoint_and_server_key(supabase_settings):
    url = await storage.upload_image("properties/7/photo.jpg", b"jpeg", "image/jpeg")

    assert url == "https://example.supabase.co/storage/v1/object/public/property-images/properties/7/photo.jpg"
    method, endpoint, kwargs = FakeClient.calls[0]
    assert method == "POST"
    assert endpoint.endswith("/storage/v1/object/property-images/properties/7/photo.jpg")
    assert kwargs["content"] == b"jpeg"
    assert kwargs["headers"]["Authorization"] == "Bearer server-secret"
    assert kwargs["headers"]["x-upsert"] == "false"


@pytest.mark.asyncio
async def test_supabase_delete_uses_remove_object_endpoint(supabase_settings):
    url = "https://example.supabase.co/storage/v1/object/public/property-images/properties/7/photo.jpg"
    await storage.delete_image(url)

    method, endpoint, kwargs = FakeClient.calls[0]
    assert method == "DELETE"
    assert endpoint.endswith("/storage/v1/object/property-images")
    assert kwargs["json"] == {"prefixes": ["properties/7/photo.jpg"]}
    assert kwargs["headers"]["Authorization"] == "Bearer server-secret"


@pytest.mark.asyncio
async def test_supabase_delete_rejects_path_traversal(supabase_settings):
    url = "https://example.supabase.co/storage/v1/object/public/property-images/properties/../secret.jpg"
    with pytest.raises(storage.StorageError, match="Invalid Supabase Storage object path"):
        await storage.delete_image(url)
    assert FakeClient.calls == []


@pytest.mark.asyncio
async def test_supabase_upload_failure_raises_storage_error(supabase_settings):
    FakeClient.response = FakeResponse(500)
    try:
        with pytest.raises(storage.StorageError, match="upload failed"):
            await storage.upload_image("properties/7/photo.jpg", b"jpeg", "image/jpeg")
    finally:
        FakeClient.response = FakeResponse(200)


@pytest.mark.asyncio
async def test_supabase_delete_failure_raises_storage_error(supabase_settings):
    FakeClient.response = FakeResponse(500)
    try:
        with pytest.raises(storage.StorageError, match="delete failed"):
            await storage.delete_image("https://example.supabase.co/storage/v1/object/public/property-images/properties/7/photo.jpg")
    finally:
        FakeClient.response = FakeResponse(200)
