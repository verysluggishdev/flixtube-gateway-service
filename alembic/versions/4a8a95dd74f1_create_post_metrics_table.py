"""Create post metrics table

Revision ID: 4a8a95dd74f1
Revises: 71af2d52a9d4
Create Date: 2023-12-27 14:07:04.743927

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a8a95dd74f1'
down_revision: Union[str, None] = '71af2d52a9d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('post_metrics',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('liked', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('disliked', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('shared', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                    server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('user_id', 'post_id'),
    )
    op.create_foreign_key('postmetrics_users_fk', source_table="post_metrics", referent_table="users", local_cols=[
                          'user_id'], remote_cols=['id'], ondelete="CASCADE")
    op.create_foreign_key('postmetrics_posts_fk', source_table="post_metrics", referent_table="posts", local_cols=[
                          'post_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_table('post_metrics')
