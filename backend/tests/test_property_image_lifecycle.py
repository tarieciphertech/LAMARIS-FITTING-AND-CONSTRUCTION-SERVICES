import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import get_current_user
from app.db.models import PropertyImage, User
from app.db.session import Base, get_db
from app.main import app
import app.api.routes.properties as properties_route
from app.services.storage import StorageError


@pytest.fixture()
def client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    with Session() as db:
        admin = User(email="image-admin@example.com", password_hash="test", is_active=True)
        db.add(admin)
        db.commit()
        db.refresh(admin)

    def override_db():
        with Session() as session:
            yield session

    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_current_user] = lambda: admin

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    engine.dispose()


def property_payload(slug="image-test-property"):
    return {
        "title": "Image Test Property",
        "slug": slug,
        "property_type": "House",
        "location": "Harare",
        "price": "USD 100,000",
        "bedrooms": 3,
        "rooms": 5,
        "stand_size": "400 sqm",
        "description": "Test property",
        "features": "Garage",
        "paperwork_status": "Ready",
        "status": "available",
        "featured": False,
    }


def create_property(client):
    response = client.post("/api/properties", json=property_payload())
    assert response.status_code == 201
    return response.json()["id"]


def test_upload_persists_cloudinary_url_and_public_id(client, monkeypatch):
    property_id = create_property(client)
    png = b"\x89PNG\r\n\x1a\n" + b"test-image"

    async def fake_upload(public_id, data, content_type):
        return f"https://res.cloudinary.com/demo/image/upload/{public_id}.png", public_id

    monkeypatch.setattr(properties_route, "upload_image", fake_upload)
    response = client.post(
        f"/api/properties/{property_id}/images/upload",
        files={"file": ("house.png", png, "image/png")},
    )
    assert response.status_code == 200
    image = response.json()["images"][0]
    assert image["url"].startswith("https://res.cloudinary.com/")
    assert image["storage_key"].startswith(f"lamaris/properties/{property_id}/")


def test_storage_failure_does_not_create_image_record(client, monkeypatch):
    property_id = create_property(client)

    async def fail_upload(*args, **kwargs):
        raise StorageError("storage unavailable")

    monkeypatch.setattr(properties_route, "upload_image", fail_upload)
    png = b"\x89PNG\r\n\x1a\n" + b"test-image"
    response = client.post(
        f"/api/properties/{property_id}/images/upload",
        files={"file": ("house.png", png, "image/png")},
    )
    assert response.status_code == 502
    assert client.get(f"/api/properties/{property_id}").json()["images"] == []


def test_deletion_removes_cloudinary_asset_and_database_record(client, monkeypatch):
    property_id = create_property(client)
    storage_key = f"lamaris/properties/{property_id}/photo"
    response = client.post(
        f"/api/properties/{property_id}/images/upload",
        files={"file": ("house.png", b"\x89PNG\r\n\x1a\n" + b"test-image", "image/png")},
    )
    assert response.status_code == 502  # no real Cloudinary credentials in tests

    db_engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    db_engine.dispose()

    async def fake_upload(public_id, data, content_type):
        return f"https://res.cloudinary.com/demo/image/upload/{public_id}.png", storage_key

    async def fake_delete(public_id):
        assert public_id == storage_key

    monkeypatch.setattr(properties_route, "upload_image", fake_upload)
    monkeypatch.setattr(properties_route, "delete_image", fake_delete)
    response = client.post(
        f"/api/properties/{property_id}/images/upload",
        files={"file": ("house.png", b"\x89PNG\r\n\x1a\n" + b"test-image", "image/png")},
    )
    image_id = response.json()["images"][0]["id"]

    response = client.delete(f"/api/properties/images/{image_id}")
    assert response.status_code == 204
    assert client.get(f"/api/properties/{property_id}").json()["images"] == []


def test_deletion_storage_failure_rolls_back_database_delete(client, monkeypatch):
    property_id = create_property(client)
    storage_key = f"lamaris/properties/{property_id}/photo"

    async def fake_upload(public_id, data, content_type):
        return f"https://res.cloudinary.com/demo/image/upload/{public_id}.png", storage_key

    async def fail_delete(public_id):
        raise StorageError("storage unavailable")

    monkeypatch.setattr(properties_route, "upload_image", fake_upload)
    monkeypatch.setattr(properties_route, "delete_image", fail_delete)
    response = client.post(
        f"/api/properties/{property_id}/images/upload",
        files={"file": ("house.png", b"\x89PNG\r\n\x1a\n" + b"test-image", "image/png")},
    )
    image_id = response.json()["images"][0]["id"]

    response = client.delete(f"/api/properties/images/{image_id}")
    assert response.status_code == 502
    assert client.get(f"/api/properties/{property_id}").json()["images"][0]["id"] == image_id
