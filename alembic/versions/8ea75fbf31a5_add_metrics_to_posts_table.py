"""Add metrics to posts table

Revision ID: 8ea75fbf31a5
Revises: 71af2d52a9d4
Create Date: 2023-12-27 13:25:01.482609

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ea75fbf31a5'
down_revision: Union[str, None] = '71af2d52a9d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('likes', sa.BigInteger(), server_default='0', nullable=False))
    op.add_column('posts', sa.Column('dislikes', sa.BigInteger(), server_default='0', nullable=False))
    op.add_column('posts', sa.Column('shares', sa.BigInteger(), server_default='0', nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'likes')
    op.drop_column('posts', 'dislikes')
    op.drop_column('posts', 'shares')
