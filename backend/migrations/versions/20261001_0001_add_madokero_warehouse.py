"""Add Madokero warehouse listing

Revision ID: 20261001_0001
Revises: 20260929_0006
"""

from alembic import op
import sqlalchemy as sa

revision = "20261001_0001"
down_revision = "20260929_0006"
branch_labels = None
depends_on = None

SLUG = "madokero-warehouse-for-sale"


def upgrade():
    conn = op.get_bind()
    conn.execute(
        sa.text(
            """
            INSERT INTO properties (
                title,
                slug,
                property_type,
                location,
                price,
                bedrooms,
                rooms,
                stand_size,
                description,
                features,
                paperwork_status,
                status,
                featured
            )
            SELECT
                :title,
                :slug,
                :property_type,
                :location,
                :price,
                NULL,
                NULL,
                :stand_size,
                :description,
                :features,
                NULL,
                'available',
                TRUE
            WHERE NOT EXISTS (
                SELECT 1 FROM properties WHERE slug = :slug
            )
            """
        ),
        {
            "title": "Madokero Warehouse for Sale",
            "slug": SLUG,
            "property_type": "Commercial Buildings",
            "location": "Madokero, Harare",
            "price": "US$1,000,000",
            "stand_size": "5,500 sqm",
            "description": (
                "Warehouse property for sale in Madokero, Harare, seated on "
                "5,500 sqm of land. The property includes a 2,000 sqm warehouse "
                "floor and 440 sqm of offices. Ready for use."
            ),
            "features": (
                "2,000 sqm warehouse floor; 440 sqm offices; "
                "high-clearance steel structure; ready for use."
            ),
        },
    )


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM properties WHERE slug = :slug"), {"slug": SLUG})
