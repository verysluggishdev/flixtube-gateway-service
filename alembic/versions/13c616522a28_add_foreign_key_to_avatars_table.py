"""Add foreign key to avatars table

Revision ID: 13c616522a28
Revises: c3f833347460
Create Date: 2023-12-16 12:40:35.429950

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '13c616522a28'
down_revision: Union[str, None] = 'c3f833347460'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('avatars', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('avatars_users_fk', source_table="avatars", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('avatars_users_fk', table_name="avatars")
    op.drop_column('avatars', 'owner_id')
