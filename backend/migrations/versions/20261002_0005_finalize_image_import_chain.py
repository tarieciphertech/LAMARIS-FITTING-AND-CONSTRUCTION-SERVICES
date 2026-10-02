"""Finalize the property-image import migration chain.

Revision ID: 20261002_0005
Revises: 20261002_0004
"""

from alembic import op
import sqlalchemy as sa

revision = "20261002_0005"
down_revision = "20261002_0004"
branch_labels = None
depends_on = None

def upgrade() -> None:
    # The previous migration is intentionally best-effort. This revision exists
    # to make the migration chain deterministic even when Cloudinary permissions
    # temporarily prevent media creation.
    pass

def downgrade() -> None:
    pass
