from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import get_current_user
from app.db.models import User
from app.db.session import Base, get_db
from app.main import app
import app.api.routes.properties as properties_route
from app.services.storage import StorageError


@pytest.fixture()
def client(tmp_path):
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
    properties_route.settings.upload_dir = str(tmp_path)
    properties_route.settings.supabase_url = ""
    properties_route.settings.supabase_service_role_key = ""

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


def test_upload_persists_file_and_database_record(client, tmp_path):
    property_id = create_property(client)
    png = b"\x89PNG\r\n\x1a\n" + b"test-image"
    response = client.post(
        f"/api/properties/{property_id}/images/upload",
        files={"file": ("house.png", png, "image/png")},
    )
    assert response.status_code == 200
    image = response.json()["images"][0]
    assert image["url"].startswith("/uploads/properties/")
    assert image["alt_text"] == "Image Test Property"
    stored = Path(tmp_path) / "properties" / str(property_id)
    assert len(list(stored.glob("*.png"))) == 1


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


def test_deletion_removes_storage_file_and_database_record(client, tmp_path):
    property_id = create_property(client)
    png = b"\x89PNG\r\n\x1a\n" + b"test-image"
    response = client.post(
        f"/api/properties/{property_id}/images/upload",
        files={"file": ("house.png", png, "image/png")},
    )
    image_id = response.json()["images"][0]["id"]
    stored = Path(tmp_path) / "properties" / str(property_id)
    assert len(list(stored.glob("*.png"))) == 1

    response = client.delete(f"/api/properties/images/{image_id}")

    assert response.status_code == 204
    assert list(stored.glob("*.png")) == []
    assert client.get(f"/api/properties/{property_id}").json()["images"] == []


def test_deletion_storage_failure_rolls_back_database_delete(client, monkeypatch):
    property_id = create_property(client)
    response = client.post(
        f"/api/properties/{property_id}/images",
        params={"url": "/uploads/properties/1/photo.png", "alt_text": "House"},
    )
    image_id = response.json()["images"][0]["id"]

    async def fail_delete(url):
        raise StorageError("storage unavailable")

    monkeypatch.setattr(properties_route, "delete_image", fail_delete)
    response = client.delete(f"/api/properties/images/{image_id}")

    assert response.status_code == 502
    assert client.get(f"/api/properties/{property_id}").json()["images"][0]["id"] == image_id
