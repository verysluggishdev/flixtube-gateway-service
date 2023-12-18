"""Add channelName and channelID columns to users table

Revision ID: 3b0ec1568bfb
Revises: 7a8a33a7fcfe
Create Date: 2023-12-18 16:05:29.114678

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b0ec1568bfb'
down_revision: Union[str, None] = '13c616522a28'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.add_column('users', sa.Column('channelID', sa.String(), nullable=False, unique=True))
    op.add_column('users', sa.Column('channelName', sa.String(), nullable=False))



def downgrade() -> None:
    op.drop_column('users', 'channelID')
    op.drop_column('users', 'channelName')
