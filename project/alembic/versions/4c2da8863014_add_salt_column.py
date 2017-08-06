"""add salt column

Revision ID: 4c2da8863014
Revises: 9abfe34399c9
Create Date: 2017-08-06 00:11:46.700897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c2da8863014'
down_revision = '9abfe34399c9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('salt', sa.String(22)))


def downgrade():
    op.drop_colunm('users', 'salt')
