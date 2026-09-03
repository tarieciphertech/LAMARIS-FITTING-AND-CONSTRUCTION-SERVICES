"""Harden property and property-image persistence."""
from alembic import op
import sqlalchemy as sa

revision = "20260903_0002"
down_revision = "20260903_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    property_constraints = {c["name"] for c in inspector.get_check_constraints("properties")}
    if "ck_properties_bedrooms_nonnegative" not in property_constraints:
        op.create_check_constraint(
            "ck_properties_bedrooms_nonnegative",
            "properties",
            "bedrooms IS NULL OR bedrooms >= 0",
        )
    if "ck_properties_rooms_nonnegative" not in property_constraints:
        op.create_check_constraint(
            "ck_properties_rooms_nonnegative",
            "properties",
            "rooms IS NULL OR rooms >= 0",
        )

    image_constraints = {c["name"] for c in inspector.get_check_constraints("property_images")}
    if "ck_property_images_sort_order_nonnegative" not in image_constraints:
        op.create_check_constraint(
            "ck_property_images_sort_order_nonnegative",
            "property_images",
            "sort_order >= 0",
        )

    property_indexes = {i["name"] for i in inspector.get_indexes("properties")}
    if "ix_properties_status_featured_created" not in property_indexes:
        op.create_index(
            "ix_properties_status_featured_created",
            "properties",
            ["status", "featured", "created_at"],
        )

    image_indexes = {i["name"] for i in inspector.get_indexes("property_images")}
    if "ix_property_images_property_order" not in image_indexes:
        op.create_index(
            "ix_property_images_property_order",
            "property_images",
            ["property_id", "sort_order"],
        )


def downgrade() -> None:
    op.drop_index("ix_property_images_property_order", table_name="property_images")
    op.drop_index("ix_properties_status_featured_created", table_name="properties")
    op.drop_constraint("ck_property_images_sort_order_nonnegative", "property_images", type_="check")
    op.drop_constraint("ck_properties_rooms_nonnegative", "properties", type_="check")
    op.drop_constraint("ck_properties_bedrooms_nonnegative", "properties", type_="check")
