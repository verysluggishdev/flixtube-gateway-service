"""Create posts table

Revision ID: 25be71ec8447
Revises: 3b0ec1568bfb
Create Date: 2023-12-19 10:17:21.041087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '25be71ec8447'
down_revision: Union[str, None] = '3b0ec1568bfb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',
                sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                sa.Column('title', sa.String(), nullable=False),
                sa.Column('description', sa.String(), nullable=False),
                sa.Column('thumbnail', sa.String(), nullable=False),
                sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                            server_default=sa.text('now()'), nullable=False),                    
    )


def downgrade() -> None:
    op.drop_table('posts')
