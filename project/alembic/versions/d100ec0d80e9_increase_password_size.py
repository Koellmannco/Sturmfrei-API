"""increase password size

Revision ID: d100ec0d80e9
Revises: 4c2da8863014
Create Date: 2017-08-06 01:38:02.829019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd100ec0d80e9'
down_revision = '4c2da8863014'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('users', 'password', type_=sa.String(128), existing_type=sa.String(length=32), nullable=False)


def downgrade():
    pass
