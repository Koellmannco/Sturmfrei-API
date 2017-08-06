"""drop salt column

Revision ID: ceaa45fe6fe4
Revises: d100ec0d80e9
Create Date: 2017-08-06 01:48:33.151979

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ceaa45fe6fe4'
down_revision = 'd100ec0d80e9'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('users', 'salt')


def downgrade():
    op.add_column('users', sa.Column('salt', sa.String(22)))
