"""Create posts table

Revision ID: de60c4c6f813
Revises: 
Create Date: 2024-08-25 09:06:11.409079

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de60c4c6f813'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("posts")
