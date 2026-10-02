"""Import LamarIS property photos from the dedicated GitHub image repository into Cloudinary.

Revision ID: 20261002_0003
Revises: 20261001_0002
"""

from __future__ import annotations

import hashlib
import json
import re
from urllib.parse import quote
from urllib.request import Request, urlopen

from alembic import op
import sqlalchemy as sa
import cloudinary
from cloudinary import uploader

revision = "20261002_0003"
down_revision = "20261001_0002"
branch_labels = None
depends_on = None

GITHUB_API = "https://api.github.com/repos/tarieciphertech/lamaris-property-images/git/trees/main?recursive=1"
RAW_BASE = "https://raw.githubusercontent.com/tarieciphertech/lamaris-property-images/main/"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
STOP_WORDS = {
    "property", "properties", "image", "images", "photo", "photos", "masvingo",
    "house", "stand", "for", "sale", "the", "and", "with", "sqm", "room", "rooms",
    "bedroom", "bedrooms", "unfinished", "finished", "medium", "lot", "a",
}
LOCATION_ALIASES = {
    "vic": "victoria",
    "range": "ranch",
    "victoria-ranch": "victoria ranch",
    "phase-mufamba": "mufamba",
    "paaminas": "aminas",
    "aminas": "aminas",
}


def _tokens(value: str) -> set[str]:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    raw = {x for x in value.split() if x and x not in STOP_WORDS}
    expanded = set(raw)
    for token in list(raw):
        alias = LOCATION_ALIASES.get(token)
        if alias:
            expanded.update(alias.split())
    return expanded


def _github_images() -> list[str]:
    request = Request(
        GITHUB_API,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "lamaris-image-import/1.0"},
    )
    with urlopen(request, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return [
        item["path"]
        for item in payload.get("tree", [])
        if item.get("type") == "blob"
        and any(item.get("path", "").lower().endswith(ext) for ext in IMAGE_EXTENSIONS)
    ]


def _score(property_row: dict, path: str) -> int:
    property_tokens = _tokens(
        " ".join(
            [
                property_row["title"] or "",
                property_row["slug"] or "",
                property_row["location"] or "",
                property_row["property_type"] or "",
            ]
        )
    )
    path_tokens = _tokens(path.rsplit("/", 1)[-1])
    path_text = path.lower()
    score = len(property_tokens & path_tokens)

    # Location names are the strongest useful signal for this repo's listing photos.
    location_tokens = _tokens(property_row["location"] or "")
    score += 3 * len(location_tokens & path_tokens)

    # Preserve distinctive numeric clues such as 588, 4800, 7, 8, 9, 2000, 5500.
    numeric = set(re.findall(r"\d+", (property_row["title"] or "") + " " + (property_row["slug"] or "") + " " + (property_row["stand_size"] or "")))
    score += 2 * len(numeric & set(re.findall(r"\d+", path_text)))
    return score


def upgrade() -> None:
    bind = op.get_bind()
    settings = bind.execute(
        sa.text(
            "SELECT current_setting('app.cloudinary_cloud_name', true), "
            "current_setting('app.cloudinary_api_key', true), "
            "current_setting('app.cloudinary_api_secret', true)"
        )
    ).one_or_none()

    # Render does not expose arbitrary env vars through PostgreSQL settings. The
    # actual upload credentials are injected by the application environment, so
    # configure Cloudinary from the same environment variables used by the API.
    import os

    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    api_key = os.getenv("CLOUDINARY_API_KEY", "")
    api_secret = os.getenv("CLOUDINARY_API_SECRET", "")
    if not (cloud_name and api_key and api_secret):
        return

    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
        secure=True,
    )

    image_paths = _github_images()
    if not image_paths:
        return

    rows = bind.execute(
        sa.text(
            "SELECT id, title, slug, location, property_type, stand_size "
            "FROM properties WHERE status IN ('available','sold') ORDER BY id"
        )
    ).mappings().all()

    for row in rows:
        existing = bind.execute(
            sa.text("SELECT COUNT(*) FROM property_images WHERE property_id = :property_id"),
            {"property_id": row["id"]},
        ).scalar_one()
        if existing:
            continue

        candidates = sorted(
            ((path, _score(row, path)) for path in image_paths),
            key=lambda item: (-item[1], item[0]),
        )

        # Only import photos with a meaningful filename match. This prevents
        # unrelated branding/hero images from being attached to listings.
        selected = [path for path, score in candidates if score >= 4][:30]
        for sort_order, path in enumerate(selected):
            filename = path.rsplit("/", 1)[-1]
            digest = hashlib.sha1(path.encode("utf-8")).hexdigest()[:12]
            public_id = f"lamaris/properties/{row['id']}/{digest}"
            raw_url = RAW_BASE + quote(path, safe="/")
            try:
                result = uploader.upload(
                    raw_url,
                    public_id=public_id,
                    asset_folder=f"lamaris/properties/{row['id']}",
                    resource_type="image",
                    overwrite=False,
                    unique_filename=False,
                    use_filename=False,
                    invalidate=True,
                )
                secure_url = result.get("secure_url")
                returned_public_id = result.get("public_id")
                if not secure_url or not returned_public_id:
                    continue
                alt = f"{row['title']} property photo"
                bind.execute(
                    sa.text(
                        "INSERT INTO property_images "
                        "(property_id, url, storage_key, alt_text, sort_order) "
                        "VALUES (:property_id, :url, :storage_key, :alt_text, :sort_order)"
                    ),
                    {
                        "property_id": row["id"],
                        "url": secure_url,
                        "storage_key": returned_public_id,
                        "alt_text": alt,
                        "sort_order": sort_order,
                    },
                )
            except Exception:
                # A bad individual source image must not prevent the rest of the
                # production migration from completing.
                continue


def downgrade() -> None:
    # Images are intentionally not deleted from Cloudinary during downgrade.
    # Remove only the DB references created by this migration's public-id prefix.
    bind = op.get_bind()
    bind.execute(
        sa.text(
            "DELETE FROM property_images "
            "WHERE storage_key LIKE 'lamaris/properties/%'"
        )
    )
