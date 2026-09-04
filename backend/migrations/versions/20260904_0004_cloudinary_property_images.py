"""Store Cloudinary public IDs for property images."""
from alembic import op
import sqlalchemy as sa

revision = "20260904_0004"
down_revision = "20260903_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {column["name"] for column in inspector.get_columns("property_images")}
    if "storage_key" not in columns:
        op.add_column(
            "property_images",
            sa.Column("storage_key", sa.String(length=255), nullable=True),
        )

    indexes = {index["name"] for index in inspector.get_indexes("property_images")}
    if "ix_property_images_storage_key" not in indexes:
        op.create_index(
            "ix_property_images_storage_key",
            "property_images",
            ["storage_key"],
        )


def downgrade() -> None:
    op.drop_index("ix_property_images_storage_key", table_name="property_images")
    op.drop_column("property_images", "storage_key")
