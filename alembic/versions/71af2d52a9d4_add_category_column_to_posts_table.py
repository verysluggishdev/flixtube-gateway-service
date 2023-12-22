"""Add category column to posts table

Revision ID: 71af2d52a9d4
Revises: 42b382ca475f
Create Date: 2023-12-22 13:10:41.988211

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71af2d52a9d4'
down_revision: Union[str, None] = '42b382ca475f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('category', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'category')
