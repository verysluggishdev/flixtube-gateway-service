"""Add video column to posts table

Revision ID: 1d223920a36a
Revises: 67ca1b4adbaf
Create Date: 2023-12-19 14:47:31.806047

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d223920a36a'
down_revision: Union[str, None] = '67ca1b4adbaf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('video', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'video')
