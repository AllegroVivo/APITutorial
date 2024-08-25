"""Add FK to 'posts'

Revision ID: b9c2e4a779c7
Revises: ea119089ff0b
Create Date: 2024-08-25 09:24:35.579068

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9c2e4a779c7'
down_revision: Union[str, None] = 'ea119089ff0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key("posts_users_fk", 'posts', 'users', ['owner_id'], ['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
