"""Seed the initial Masvingo land listings."""

from alembic import op
import sqlalchemy as sa

revision = "20260929_0005"
down_revision = "20260904_0004"
branch_labels = None
depends_on = None

PROPERTIES = [
    {
        "title": "Morningside 1.9 Hectare Plot",
        "slug": "morningside-1-9-hectare-plot",
        "location": "Morningside, Masvingo",
        "price": "US$27,500",
        "size": "1.9 hectares",
        "description": "1.9-hectare property available in Morningside, Masvingo. Title deeds are indicated as available.",
        "features": "1.9 hectares; Morningside; Masvingo; Title Deeds",
        "paperwork": "Title Deeds",
    },
    {
        "title": "Zishumbe 50 Hectare Plot",
        "slug": "zishumbe-50-hectare-plot",
        "location": "Zishumbe, Masvingo",
        "price": "US$78,000",
        "size": "50 hectares",
        "description": "50-hectare property available in Zishumbe, Masvingo. Title deeds are indicated as available.",
        "features": "50 hectares; Zishumbe; Masvingo; Title Deeds",
        "paperwork": "Title Deeds",
    },
    {
        "title": "Gutu Turn Off 20 Hectare Plot",
        "slug": "gutu-turn-off-20-hectare-plot",
        "location": "Gutu Turn Off, Masvingo",
        "price": "US$68,000",
        "size": "20 hectares",
        "description": "20-hectare property available at Gutu Turn Off, Masvingo. Title deeds are indicated as available.",
        "features": "20 hectares; Gutu Turn Off; Masvingo; Title Deeds",
        "paperwork": "Title Deeds",
    },
    {
        "title": "Morningside 1.3 Hectare Plot",
        "slug": "morningside-1-3-hectare-plot",
        "location": "Morningside, Masvingo",
        "price": "US$30,000",
        "size": "1.3 hectares",
        "description": "1.3-hectare property available in Morningside, Masvingo. Government lease is indicated as available and ready for deeds.",
        "features": "1.3 hectares; Morningside; Masvingo; Government Lease; Ready for Deeds",
        "paperwork": "Government Lease — Ready for Deeds",
    },
    {
        "title": "Chihovhorosi 20 Hectare Plot - US$30,000",
        "slug": "chihovhorosi-20-hectare-plot-30000",
        "location": "Chihovhorosi, Masvingo",
        "price": "US$30,000",
        "size": "20 hectares",
        "description": "20-hectare property available in Chihovhorosi, Masvingo. Offer letter is indicated as the available documentation.",
        "features": "20 hectares; Chihovhorosi; Masvingo; Offer Letter",
        "paperwork": "Offer Letter",
    },
    {
        "title": "Chihovhorosi 10 Hectare Plot",
        "slug": "chihovhorosi-10-hectare-plot",
        "location": "Chihovhorosi, Masvingo",
        "price": "US$15,000",
        "size": "10 hectares",
        "description": "10-hectare property available in Chihovhorosi, Masvingo. Offer letter is indicated as the available documentation.",
        "features": "10 hectares; Chihovhorosi; Masvingo; Offer Letter",
        "paperwork": "Offer Letter",
    },
    {
        "title": "Chihovhorosi 20 Hectare Plot - US$28,000",
        "slug": "chihovhorosi-20-hectare-plot-28000",
        "location": "Chihovhorosi, Masvingo",
        "price": "US$28,000",
        "size": "20 hectares",
        "description": "20-hectare property available in Chihovhorosi, Masvingo. Offer letter is indicated as the available documentation.",
        "features": "20 hectares; Chihovhorosi; Masvingo; Offer Letter",
        "paperwork": "Offer Letter",
    },
    {
        "title": "Mutimurefu 10 Hectare Plot",
        "slug": "mutimurefu-10-hectare-plot",
        "location": "Mutimurefu, Masvingo",
        "price": "US$14,000",
        "size": "10 hectares",
        "description": "10-hectare property available in Mutimurefu, Masvingo. Offer letter is indicated as the available documentation.",
        "features": "10 hectares; Mutimurefu; Masvingo; Offer Letter",
        "paperwork": "Offer Letter",
    },
    {
        "title": "Roy 20 Hectare Plot",
        "slug": "roy-20-hectare-plot",
        "location": "Roy, Masvingo",
        "price": "US$25,000",
        "size": "20 hectares",
        "description": "20-hectare property available in Roy, Masvingo. Offer letter is indicated as the available documentation.",
        "features": "20 hectares; Roy; Masvingo; Offer Letter",
        "paperwork": "Offer Letter",
    },
    {
        "title": "Mazare 10 Hectare Plot",
        "slug": "mazare-10-hectare-plot",
        "location": "Mazare, Masvingo",
        "price": "US$12,000",
        "size": "10 hectares",
        "description": "10-hectare property available in Mazare, Masvingo. Offer letter is indicated as the available documentation.",
        "features": "10 hectares; Mazare; Masvingo; Offer Letter",
        "paperwork": "Offer Letter",
    },
    {
        "title": "Zishumbe 10 Hectare Plot",
        "slug": "zishumbe-10-hectare-plot",
        "location": "Zishumbe, Masvingo",
        "price": "US$12,000",
        "size": "10 hectares",
        "description": "10-hectare property available in Zishumbe, Masvingo. Offer letter is indicated as the available documentation.",
        "features": "10 hectares; Zishumbe; Masvingo; Offer Letter",
        "paperwork": "Offer Letter",
    },
    {
        "title": "Zishumbe 15 Hectare Plot",
        "slug": "zishumbe-15-hectare-plot",
        "location": "Zishumbe, Masvingo",
        "price": "US$17,000",
        "size": "15 hectares",
        "description": "15-hectare property available in Zishumbe, Masvingo. Offer letter is indicated as the available documentation.",
        "features": "15 hectares; Zishumbe; Masvingo; Offer Letter",
        "paperwork": "Offer Letter",
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
                property_type="Land",
                location=item["location"],
                price=item["price"],
                bedrooms=None,
                rooms=None,
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
