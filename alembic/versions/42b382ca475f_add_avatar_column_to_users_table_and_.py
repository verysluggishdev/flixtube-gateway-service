"""Add avatar column to users table and drop avatars table

Revision ID: 42b382ca475f
Revises: 1d223920a36a
Create Date: 2023-12-20 11:43:53.763832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42b382ca475f'
down_revision: Union[str, None] = '1d223920a36a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('avatars')
    op.add_column('users', sa.Column('avatar', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('users', 'avatar')
    op.create_table('avatars',
                sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                sa.Column('filename', sa.String(), nullable=False, unique=True),
                sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                            server_default=sa.text('now()'), nullable=False),
    )
