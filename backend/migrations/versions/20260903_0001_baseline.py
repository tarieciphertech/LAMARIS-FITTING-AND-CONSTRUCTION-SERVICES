"""Baseline LamarIS database schema.

This migration is intentionally safe for the current MVP database: the app
previously used SQLAlchemy create_all(), so existing installations may already
have the tables. create_all() fills missing tables while the explicit
column check handles the token_version field added for JWT invalidation.
"""
from alembic import op
import sqlalchemy as sa

revision = "20260903_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()

    # Import the authoritative ORM metadata and create any missing tables.
    # Existing tables are left untouched by SQLAlchemy create_all().
    from app.db.session import Base
    from app.db import models  # noqa: F401
    Base.metadata.create_all(bind=bind)

    inspector = sa.inspect(bind)
    user_columns = {column["name"] for column in inspector.get_columns("users")}
    if "token_version" not in user_columns:
        op.add_column(
            "users",
            sa.Column("token_version", sa.Integer(), nullable=False, server_default="0"),
        )
        op.alter_column("users", "token_version", server_default=None)


def downgrade() -> None:
    # Baseline migrations must not destroy production data. Future migrations
    # should provide their own reversible downgrade operations.
    pass
