"""Import the supplied LamarIS property-photo repository into Cloudinary.

Revision ID: 20261002_0003
Revises: 20261001_0002
"""

from __future__ import annotations

import os
from urllib.parse import quote

from alembic import op
import cloudinary
from cloudinary import uploader
import sqlalchemy as sa

revision = "20261002_0003"
down_revision = "20261001_0002"
branch_labels = None
depends_on = None

RAW_BASE = "https://raw.githubusercontent.com/tarieciphertech/lamaris-property-images/main/"

IMAGE_MAP = {
    "madokero-warehouse-for-sale": " MADOKERO WAREHOUSE FOR SALE.jpeg",
    "7-room-unfinished-house-takawira-masvingo-16000": "7 ROOMED UNFINISHED HOUSE - TAKAWIRA, MASVINGO\n\n- Property: 7 Rooms, At Window Level \n- Developer: Unibrik\n- Size: 300 Square Metres\n- Location: Takawira, Masvingo.jpeg",
    "8-room-house-victoria-ranch-masvingo-45000": "8 ROOMS - VICTORIA RANCH, MASVINGO\n\n- Property: 8 Rooms\n- Size: 250 Square Metres\n- Location: Victoria Ranch, Near Jazire Creche, Masvingo.jpeg",
    "8-room-house-kmp-masvingo-46000": "8-ROOMS FOR SALE - KMP, MASVINGO - $46,000.jpeg",
    "9-room-house-pambudzi-masvingo-65000": "9-ROOMED HOUSE FOR SALE - PAMBUDZI, MASVINGO .jpeg",
    "4800sqm-stand-westview-industrial-masvingo-150000": "GO - 4800M² STAND, WESTVIEW INDUSTRIAL, MASVINGO\n\n- Size: 4,800 Square Metres\n- Location: Westview Industrial Area, Masvingo",
    "240sqm-commercial-stand-lot-a-masvingo-8000": "LOT A COMMERCIAL - 240sqm - $8,000.jpeg",
    "5-room-semi-detached-house-sisk-masvingo-35000": "QUICK SALE MASVINGO - 5 ROOMED SEMI-DETACHED - $35,000.jpeg",
    "7-bedroom-unfinished-house-zimre-park-masvingo-120000": "UNFINISHED 7 BEDROOMED HOUSE - ZIMRE PARK, MASVINGO\n\nLow Density\nStand Size: 2000sqm\nBedrooms: 7\nLocation: Close to GZU Campus\n.jpeg",
    "588sqm-stand-zexcom-masvingo-12000": "ZEXCOM - 588sqm - $12,000.jpeg",
    "sports-bar-for-sale-paaminas-masvingo-90000": "🍺🏟️ SPORTS BAR FOR SALE - @ AMINAS, MASVINGO\n\n- 📍 Location: PaAminas, Masvingo (Prime Business Location)\n- 🏢 Property: Sports Bar for Sale\n- 📐 Size: 300 Square Metres\n- 💸 Price: $90,000 USD 🇺🇸.jpeg",
    "300sqm-stand-rujeko-masvingo-12500": "🏜️ EMERGENCY SALE (STAND) - MASVINGO\n\n- 📍 Location: Rujeko, Masvingo\n- 📐 Size: 300sqm\n- 🛣️ Features: Tarred Roads ✅\n- 🗂️ Paperwork: Council Cession\n- 💸 Price: $12,500 USD 🇺🇸.jpeg",
    "7-room-house-zexcom-masvingo-20000": "🏠 HOUSE FOR SALE - ZEXCOM, MASVINGO\n\n- 📍 Location: Zexcom, Masvingo\n- 📐 Stand Size: 460m² (Medium Density)\n- 🏘️ Description: 7 Rooms House\n- 🗂️ Paperwork: Council Cession\n- 💸 Price: $20,000 USD .jpeg",
}

def upgrade() -> None:
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    api_key = os.getenv("CLOUDINARY_API_KEY", "")
    api_secret = os.getenv("CLOUDINARY_API_SECRET", "")
    if not (cloud_name and api_key and api_secret):
        return

    cloudinary.config(cloud_name=cloud_name, api_key=api_key, api_secret=api_secret, secure=True)
    bind = op.get_bind()

    for slug, filename in IMAGE_MAP.items():
        row = bind.execute(
            sa.text("SELECT id, title FROM properties WHERE slug = :slug"),
            {"slug": slug},
        ).mappings().first()
        if not row:
            continue
        if bind.execute(
            sa.text("SELECT COUNT(*) FROM property_images WHERE property_id = :property_id"),
            {"property_id": row["id"]},
        ).scalar_one():
            continue

        raw_url = RAW_BASE + quote(filename, safe="/")
        public_id = f"lamaris/properties/{row['id']}/source-{abs(hash(filename))}"
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
            bind.execute(
                sa.text(
                    "INSERT INTO property_images "
                    "(property_id, url, storage_key, alt_text, sort_order) "
                    "VALUES (:property_id, :url, :storage_key, :alt_text, 0)"
                ),
                {
                    "property_id": row["id"],
                    "url": secure_url,
                    "storage_key": returned_public_id,
                    "alt_text": f"{row['title']} property photo",
                },
            )
        except Exception:
            continue
    bind.commit()

def downgrade() -> None:
    bind = op.get_bind()
    bind.execute(
        sa.text(
            "DELETE FROM property_images WHERE storage_key LIKE 'lamaris/properties/%/source-%'"
        )
    )
