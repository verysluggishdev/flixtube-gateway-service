"""Create subscribers table

Revision ID: 48604006f42b
Revises: fbdc848610f4
Create Date: 2024-01-04 14:37:15.512339

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48604006f42b'
down_revision: Union[str, None] = 'fbdc848610f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('subscribers',
        sa.Column('user_id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('subscribed_to', sa.Integer(), nullable=False, primary_key=True),
    )

    op.create_foreign_key('subscriber_users_fk', source_table="subscribers", referent_table="users", local_cols=[
                          'user_id'], remote_cols=['id'], ondelete="CASCADE")
    op.create_foreign_key('subscribed_to_users_fk', source_table="subscribers", referent_table="users", local_cols=[
                          'subscribed_to'], remote_cols=['id'], ondelete="CASCADE")
    

def downgrade() -> None:
    op.drop_table('subscribers')
