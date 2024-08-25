"""Add additional columns to 'posts'

Revision ID: d6749a7de426
Revises: b9c2e4a779c7
Create Date: 2024-08-25 09:29:01.706083

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6749a7de426'
down_revision: Union[str, None] = 'b9c2e4a779c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean, nullable=False, server_default="TRUE"))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.func.now()))


def downgrade() -> None:
    op.drop_column("posts", "created_at")
    op.drop_column("posts", "published")
