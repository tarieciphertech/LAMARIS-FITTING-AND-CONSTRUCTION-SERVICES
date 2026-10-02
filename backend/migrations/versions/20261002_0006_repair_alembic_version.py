"""Repair the Alembic version marker after the best-effort image import.

Revision ID: 20261002_0006
Revises: 20261002_0005
"""

from alembic import op
import sqlalchemy as sa

revision = "20261002_0006"
down_revision = "20261002_0005"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute(
        sa.text(
            "UPDATE alembic_version SET version_num = '20261002_0006' "
            "WHERE version_num = '20261002_0003'"
        )
    )

def downgrade() -> None:
    op.execute(
        sa.text(
            "UPDATE alembic_version SET version_num = '20261002_0003' "
            "WHERE version_num = '20261002_0006'"
        )
    )
