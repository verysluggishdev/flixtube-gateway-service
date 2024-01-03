"""Add channelDescription to users table

Revision ID: fbdc848610f4
Revises: 4a8a95dd74f1
Create Date: 2024-01-03 09:30:59.619226

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fbdc848610f4'
down_revision: Union[str, None] = '4a8a95dd74f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('channelDescription', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'channelDescription')
