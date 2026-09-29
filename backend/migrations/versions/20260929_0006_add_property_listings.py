"""Seed additional Lamaris property listings supplied on 26-28 September 2026."""

from alembic import op
import sqlalchemy as sa

revision = "20260929_0006"
down_revision = "20260929_0005"
branch_labels = None
depends_on = None

PROPERTIES = [
    {
        "title": "7-Room House for Sale - Zexcom, Masvingo",
        "slug": "7-room-house-zexcom-masvingo-20000",
        "property_type": "House",
        "location": "Zexcom, Masvingo",
        "price": "US$20,000",
        "size": "460 m²",
        "bedrooms": None,
        "rooms": 7,
        "description": "7-room house for sale in Zexcom, Masvingo, on a 460 m² medium-density stand. Council cession is indicated as the available paperwork. All verifications are to be completed before payment.",
        "features": "460 m²; Medium Density; 7 Rooms; Council Cession",
        "paperwork": "Council Cession",
    },
    {
        "title": "300 m² Stand for Sale - Rujeko, Masvingo",
        "slug": "300sqm-stand-rujeko-masvingo-12500",
        "property_type": "Land",
        "location": "Rujeko, Masvingo",
        "price": "US$12,500",
        "size": "300 m²",
        "bedrooms": None,
        "rooms": None,
        "description": "300 m² stand for sale in Rujeko, Masvingo. Tarred roads are indicated as a feature and council cession is indicated as the available paperwork. All verifications are to be completed before payment.",
        "features": "300 m²; Tarred Roads; Council Cession",
        "paperwork": "Council Cession",
    },
    {
        "title": "4-Room House for Sale - Rujeko A, Masvingo",
        "slug": "4-room-house-rujeko-a-masvingo-35000",
        "property_type": "House",
        "location": "Rujeko A, Masvingo",
        "price": "US$35,000",
        "size": "350 m²",
        "bedrooms": None,
        "rooms": 4,
        "description": "4-room house for sale in Rujeko A, Masvingo, on a 350 m² stand. The listing states that sewer, electricity and water are connected and that the property is within walking distance of town. All verifications are to be completed before payment.",
        "features": "350 m²; 4 Rooms; Sewer Connected; Electricity Connected; Water Connected; Walking Distance to Town",
        "paperwork": "Not stated",
    },
    {
        "title": "1140 Hectare Land - Kwekwe-Gokwe Road",
        "slug": "1140-hectare-land-kwekwe-gokwe-road-1500000",
        "property_type": "Land",
        "location": "Kwekwe-Gokwe Road, 70 km from Kwekwe",
        "price": "US$1,500,000",
        "size": "1140 hectares",
        "bedrooms": None,
        "rooms": None,
        "description": "1140-hectare land parcel located about 70 km from Kwekwe along Gokwe Road. Title deeds are indicated as available. Seller-listed price is US$1.5 million.",
        "features": "1140 hectares; 70 km from Kwekwe; Kwekwe-Gokwe Road; Title Deeds",
        "paperwork": "Title Deeds",
    },
    {
        "title": "400 Hectare Land - Chaka",
        "slug": "400-hectare-land-chaka-820000",
        "property_type": "Land",
        "location": "Chaka",
        "price": "US$820,000",
        "size": "400 hectares",
        "bedrooms": None,
        "rooms": None,
        "description": "400-hectare land parcel in Chaka. Title deeds are indicated as available.",
        "features": "400 hectares; Chaka; Title Deeds",
        "paperwork": "Title Deeds",
    },
    {
        "title": "200 Hectare Land - Zishumbe, Mutare",
        "slug": "200-hectare-land-zishumbe-mutare-680000",
        "property_type": "Land",
        "location": "Zishumbe, Mutare, 6 km from Mutare",
        "price": "US$680,000",
        "size": "200 hectares",
        "bedrooms": None,
        "rooms": None,
        "description": "200-hectare land parcel at Zishumbe, approximately 6 km from Mutare. Title deeds are indicated as available.",
        "features": "200 hectares; Zishumbe; 6 km from Mutare; Title Deeds",
        "paperwork": "Title Deeds",
    },
    {
        "title": "500 Hectare Land - Mashava",
        "slug": "500-hectare-land-mashava-1200000",
        "property_type": "Land",
        "location": "Mashava, 5 km from Mashava",
        "price": "US$1,200,000",
        "size": "500 hectares",
        "bedrooms": None,
        "rooms": None,
        "description": "500-hectare land parcel approximately 5 km from Mashava. Title deeds are indicated as available.",
        "features": "500 hectares; 5 km from Mashava; Title Deeds",
        "paperwork": "Title Deeds",
    },
    {
        "title": "200 Hectare Land - Mvuma",
        "slug": "200-hectare-land-mvuma-180000",
        "property_type": "Land",
        "location": "Mvuma",
        "price": "US$180,000",
        "size": "200 hectares",
        "bedrooms": None,
        "rooms": None,
        "description": "200-hectare land parcel in Mvuma. The source listing does not specify the paperwork, so documentation is recorded as not stated pending verification.",
        "features": "200 hectares; Mvuma",
        "paperwork": "Not stated",
    },
    {
        "title": "586 Hectare Land - Banket Highway",
        "slug": "586-hectare-land-banket-highway-1700000",
        "property_type": "Land",
        "location": "Banket, along Highway",
        "price": "US$1,700,000",
        "size": "586 hectares",
        "bedrooms": None,
        "rooms": None,
        "description": "586-hectare land parcel along the Banket highway. The listing states clean paperwork, water access through Biri Dam and Mazvikadei Dam, and 100% underground piping installed. It is described as suitable for residential development.",
        "features": "586 hectares; Along Highway; Clean Paperwork; Biri Dam; Mazvikadei Dam; 100% Underground Piping; Residential Development",
        "paperwork": "Clean Paperwork",
    },
]


def upgrade() -> None:
    properties = sa.table(
        "properties",
        sa.column("title", sa.String),
        sa.column("slug", sa.String),
        sa.column("property_type", sa.String),
        sa.column("location", sa.String),
        sa.column("price", sa.String),
        sa.column("stand_size", sa.String),
        sa.column("bedrooms", sa.Integer),
        sa.column("rooms", sa.Integer),
        sa.column("description", sa.Text),
        sa.column("features", sa.Text),
        sa.column("paperwork_status", sa.String),
        sa.column("status", sa.Enum("draft", "available", "sold", "archived", name="propertystatus", create_type=False)),
        sa.column("featured", sa.Boolean),
    )

    bind = op.get_bind()
    for item in PROPERTIES:
        exists = bind.execute(
            sa.text("SELECT 1 FROM properties WHERE slug = :slug"),
            {"slug": item["slug"]},
        ).scalar()
        if exists:
            continue

        bind.execute(
            properties.insert().values(
                title=item["title"],
                slug=item["slug"],
                property_type=item["property_type"],
                location=item["location"],
                price=item["price"],
                bedrooms=item["bedrooms"],
                rooms=item["rooms"],
                stand_size=item["size"],
                description=item["description"],
                features=item["features"],
                paperwork_status=item["paperwork"],
                status="available",
                featured=False,
            )
        )


def downgrade() -> None:
    bind = op.get_bind()
    bind.execute(
        sa.text("DELETE FROM properties WHERE slug = ANY(:slugs)"),
        {"slugs": [item["slug"] for item in PROPERTIES]},
    )
