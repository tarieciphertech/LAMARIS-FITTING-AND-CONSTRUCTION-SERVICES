"""Add explicit user roles for admin API authorization."""
from alembic import op
import sqlalchemy as sa

revision = "20260903_0003"
down_revision = "20260903_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {column["name"] for column in inspector.get_columns("users")}
    if "role" not in columns:
        op.add_column(
            "users",
            sa.Column("role", sa.String(length=30), nullable=False, server_default="admin"),
        )
        op.alter_column("users", "role", server_default=None)

    indexes = {index["name"] for index in inspector.get_indexes("users")}
    if "ix_users_role" not in indexes:
        op.create_index("ix_users_role", "users", ["role"])


def downgrade() -> None:
    op.drop_index("ix_users_role", table_name="users")
    op.drop_column("users", "role")
