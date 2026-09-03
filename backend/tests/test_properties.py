from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import get_current_user
from app.db.models import Property, User
from app.db.session import Base, get_db
from app.main import app
import app.api.routes.properties as properties_route


@pytest.fixture()
def client(tmp_path):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    db = Session()
    admin = User(email="admin@example.com", password_hash="test", is_active=True)
    db.add(admin)
    db.commit()
    db.refresh(admin)

    def override_db():
        session = Session()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_current_user] = lambda: admin
    properties_route.settings.upload_dir = str(tmp_path)

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    db.close()
    engine.dispose()


def payload(slug="modern-family-home"):
    return {
        "title": "Modern Family Home",
        "slug": slug,
        "property_type": "House",
        "location": "Masvingo",
        "price": "USD 120,000",
        "bedrooms": 4,
        "rooms": 6,
        "stand_size": "500 sqm",
        "description": "A modern family home.",
        "features": "Garage, borehole, fitted kitchen",
        "paperwork_status": "Council cession",
        "status": "available",
        "featured": True,
    }


def test_create_read_update_and_archive_property(client):
    response = client.post("/api/properties", json=payload())
    assert response.status_code == 201
    created = response.json()
    assert created["slug"] == "modern-family-home"
    assert created["status"] == "available"
    property_id = created["id"]

    response = client.get(f"/api/properties/{property_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Modern Family Home"

    updated = payload("modern-family-home-updated")
    updated["status"] = "sold"
    updated["featured"] = True
    response = client.patch(f"/api/properties/{property_id}", json=updated)
    assert response.status_code == 200
    assert response.json()["status"] == "sold"

    response = client.delete(f"/api/properties/{property_id}")
    assert response.status_code == 204

    response = client.get(f"/api/properties/{property_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "archived"
    assert response.json()["featured"] is False


def test_duplicate_slug_is_rejected(client):
    assert client.post("/api/properties", json=payload()).status_code == 201
    response = client.post("/api/properties", json=payload())
    assert response.status_code == 409
    assert "Slug already exists" in response.json()["detail"]


def test_invalid_property_payload_is_rejected(client):
    invalid = payload("bad slug")
    invalid["bedrooms"] = -1
    response = client.post("/api/properties", json=invalid)
    assert response.status_code == 422


def test_image_upload_is_persisted(client, tmp_path):
    response = client.post("/api/properties", json=payload())
    assert response.status_code == 201
    property_id = response.json()["id"]

    # Minimal valid PNG signature plus a small payload. The upload endpoint
    # validates the file signature before persisting it.
    png = b"\x89PNG\r\n\x1a\n" + b"test-image"
    response = client.post(
        f"/api/properties/{property_id}/images/upload",
        files={"file": ("house.png", png, "image/png")},
    )
    assert response.status_code == 200
    images = response.json()["images"]
    assert len(images) == 1
    assert images[0]["url"].startswith("/uploads/properties/")

    stored = Path(tmp_path) / "properties" / str(property_id)
    assert len(list(stored.glob("*.png"))) == 1


def test_invalid_image_signature_is_rejected(client):
    response = client.post("/api/properties", json=payload())
    property_id = response.json()["id"]
    response = client.post(
        f"/api/properties/{property_id}/images/upload",
        files={"file": ("fake.png", b"not-an-image", "image/png")},
    )
    assert response.status_code == 415
