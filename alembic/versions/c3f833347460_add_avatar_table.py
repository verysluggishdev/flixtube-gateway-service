"""add avatar table

Revision ID: c3f833347460
Revises: 5bfbafcffbbc
Create Date: 2023-12-16 12:10:01.453427

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3f833347460'
down_revision: Union[str, None] = '5bfbafcffbbc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('avatars',
                sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                sa.Column('filename', sa.String(), nullable=False, unique=True),
                sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                            server_default=sa.text('now()'), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('avatars')
