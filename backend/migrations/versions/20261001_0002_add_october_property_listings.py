"""Add October 2026 property listings

Revision ID: 20261001_0002
Revises: 20261001_0001
"""

from alembic import op
import sqlalchemy as sa

revision = "20261001_0002"
down_revision = "20261001_0001"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    listings = [
        {
            "title": "7-Bedroom Unfinished House - Zimre Park, Masvingo",
            "slug": "7-bedroom-unfinished-house-zimre-park-masvingo-120000",
            "property_type": "Houses",
            "location": "Zimre Park, Masvingo",
            "price": "US$120,000 Negotiable",
            "bedrooms": 7,
            "rooms": None,
            "stand_size": "2,000 sqm",
            "description": "Unfinished 7-bedroom house in a low-density, built-up area close to GZU Campus. Zesa and water are connected.",
            "features": "Low density; close to GZU Campus; built-up neighbourhood; Zesa connected; water connected; unfinished.",
            "paperwork_status": "Council cession, clean papers",
        },
        {
            "title": "7-Room Unfinished House - Takawira, Masvingo",
            "slug": "7-room-unfinished-house-takawira-masvingo-16000",
            "property_type": "Houses",
            "location": "Takawira, Masvingo",
            "price": "US$16,000",
            "bedrooms": None,
            "rooms": 7,
            "stand_size": "300 sqm",
            "description": "7-room unfinished house at window level in Takawira, Masvingo. Developer: Unibrik.",
            "features": "At window level; developer: Unibrik.",
            "paperwork_status": "Council cession",
        },
        {
            "title": "8-Room House - Victoria Ranch, Masvingo",
            "slug": "8-room-house-victoria-ranch-masvingo-45000",
            "property_type": "Houses",
            "location": "Victoria Ranch, near Jazire Creche, Masvingo",
            "price": "US$45,000",
            "bedrooms": None,
            "rooms": 8,
            "stand_size": "250 sqm",
            "description": "8-room property in Victoria Ranch, near Jazire Creche, Masvingo.",
            "features": "Fenced; water well.",
            "paperwork_status": "Council papers",
        },
        {
            "title": "420 m² Infill Stand - Lot A, Victoria Ranch, Masvingo",
            "slug": "420sqm-infill-stand-lot-a-victoria-ranch-masvingo-7000",
            "property_type": "Residential Stands",
            "location": "Lot A, Victoria Ranch, Masvingo",
            "price": "US$7,000",
            "bedrooms": None,
            "rooms": None,
            "stand_size": "420 sqm",
            "description": "420 m² infill stand for sale in Lot A, Victoria Ranch, Masvingo.",
            "features": "Infill stand.",
            "paperwork_status": None,
        },
        {
            "title": "7-Room House Slab - Lot A Medium, Masvingo",
            "slug": "7-room-house-slab-lot-a-medium-masvingo-12000",
            "property_type": "Houses",
            "location": "Lot A Medium, Masvingo",
            "price": "US$12,000",
            "bedrooms": None,
            "rooms": 7,
            "stand_size": "450 sqm",
            "description": "7-room unfinished house at slab level in Lot A Medium, Masvingo.",
            "features": "On slab level.",
            "paperwork_status": "Council cession",
        },
        {
            "title": "4,800 m² Stand - Westview Industrial, Masvingo",
            "slug": "4800sqm-stand-westview-industrial-masvingo-150000",
            "property_type": "Industrial Stands",
            "location": "Westview Industrial Area, Masvingo",
            "price": "US$150,000",
            "bedrooms": None,
            "rooms": None,
            "stand_size": "4,800 sqm",
            "description": "4,800 m² stand in Westview Industrial Area, Masvingo, suitable for cluster houses or development.",
            "features": "Ideal for cluster houses / development; reduced to go.",
            "paperwork_status": "Council papers",
        },
        {
            "title": "Sports Bar for Sale - PaAminas, Masvingo",
            "slug": "sports-bar-for-sale-paaminas-masvingo-90000",
            "property_type": "Commercial Buildings",
            "location": "PaAminas, Masvingo",
            "price": "US$90,000",
            "bedrooms": None,
            "rooms": None,
            "stand_size": "300 sqm",
            "description": "Sports bar for sale at PaAminas, Masvingo, in a prime business location and ready to operate.",
            "features": "Prime business location; ready to operate.",
            "paperwork_status": None,
        },
        {
            "title": "8-Room House - KMP, Masvingo",
            "slug": "8-room-house-kmp-masvingo-46000",
            "property_type": "Houses",
            "location": "KMP, Masvingo",
            "price": "US$46,000",
            "bedrooms": None,
            "rooms": 8,
            "stand_size": "350 sqm",
            "description": "Finished 8-room house in a built-up area of KMP, Masvingo. Ready for occupation.",
            "features": "Solar geyser; satellite dish; durawall; metal gate; walled and secure; ready for occupation; high rental returns.",
            "paperwork_status": "Council cession, clean papers; verification before payment",
        },
        {
            "title": "588 m² Stand - Zexcom, Masvingo",
            "slug": "588sqm-stand-zexcom-masvingo-12000",
            "property_type": "Residential Stands",
            "location": "Zexcom, Masvingo",
            "price": "US$12,000",
            "bedrooms": None,
            "rooms": None,
            "stand_size": "588 sqm",
            "description": "Residential stand in a built-up area of Zexcom, Masvingo, ready to build.",
            "features": "Built-up area; ready to build.",
            "paperwork_status": "Council cession; verification before payment",
        },
        {
            "title": "240 m² Commercial Stand - Lot A, Masvingo",
            "slug": "240sqm-commercial-stand-lot-a-masvingo-8000",
            "property_type": "Commercial Stands",
            "location": "Lot A Commercial, Masvingo",
            "price": "US$8,000",
            "bedrooms": None,
            "rooms": None,
            "stand_size": "240 sqm",
            "description": "Commercial stand in Masvingo with ZESA poles available and ready to build.",
            "features": "ZESA poles available; ready to build.",
            "paperwork_status": "Council cession",
        },
        {
            "title": "2-Room House - Phase Mufamba, Victoria Ranch",
            "slug": "2-room-house-phase-mufamba-victoria-ranch-13000",
            "property_type": "Houses",
            "location": "Phase Mufamba, Victoria Ranch, Masvingo",
            "price": "US$13,000",
            "bedrooms": None,
            "rooms": 2,
            "stand_size": None,
            "description": "2-room property for sale in Phase Mufamba, Victoria Ranch, Masvingo.",
            "features": None,
            "paperwork_status": None,
        },
        {
            "title": "5-Room Semi-Detached House - Sisk, Masvingo",
            "slug": "5-room-semi-detached-house-sisk-masvingo-35000",
            "property_type": "Houses",
            "location": "Sisk, Masvingo",
            "price": "US$35,000",
            "bedrooms": None,
            "rooms": 5,
            "stand_size": "250 sqm",
            "description": "5-room semi-detached house in Sisk, Masvingo.",
            "features": "Fully serviced; ZESA; sewer; tarred roads; water.",
            "paperwork_status": "Council papers",
        },
        {
            "title": "9-Room House - Pambudzi, Masvingo",
            "slug": "9-room-house-pambudzi-masvingo-65000",
            "property_type": "Houses",
            "location": "Pambudzi, Masvingo",
            "price": "US$65,000",
            "bedrooms": None,
            "rooms": 9,
            "stand_size": "525 sqm",
            "description": "9-room house in a built-up neighbourhood of Pambudzi, Masvingo. Ready to move in.",
            "features": "ZESA connected; built-up neighbourhood; ready to move in; good investment.",
            "paperwork_status": "Council cession; clean papers; admin fee paid",
        },
    ]

    for item in listings:
        conn.execute(
            sa.text(
                """
                INSERT INTO properties
                (title, slug, property_type, location, price, bedrooms, rooms,
                 stand_size, description, features, paperwork_status, status, featured)
                VALUES
                (:title, :slug, :property_type, :location, :price, :bedrooms, :rooms,
                 :stand_size, :description, :features, :paperwork_status,
                 CAST('available' AS propertystatus), FALSE)
                ON CONFLICT (slug) DO NOTHING
                """
            ),
            item,
        )


def downgrade():
    conn = op.get_bind()
    slugs = [
        "7-bedroom-unfinished-house-zimre-park-masvingo-120000",
        "7-room-unfinished-house-takawira-masvingo-16000",
        "8-room-house-victoria-ranch-masvingo-45000",
        "420sqm-infill-stand-lot-a-victoria-ranch-masvingo-7000",
        "7-room-house-slab-lot-a-medium-masvingo-12000",
        "4800sqm-stand-westview-industrial-masvingo-150000",
        "sports-bar-for-sale-paaminas-masvingo-90000",
        "8-room-house-kmp-masvingo-46000",
        "588sqm-stand-zexcom-masvingo-12000",
        "240sqm-commercial-stand-lot-a-masvingo-8000",
        "2-room-house-phase-mufamba-victoria-ranch-13000",
        "5-room-semi-detached-house-sisk-masvingo-35000",
        "9-room-house-pambudzi-masvingo-65000",
    ]
    conn.execute(
        sa.text("DELETE FROM properties WHERE slug = ANY(:slugs)"),
        {"slugs": slugs},
    )
