"""Add 'content' to posts table

Revision ID: 47dffb56cbab
Revises: de60c4c6f813
Create Date: 2024-08-25 09:14:06.404475

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47dffb56cbab'
down_revision: Union[str, None] = 'de60c4c6f813'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
