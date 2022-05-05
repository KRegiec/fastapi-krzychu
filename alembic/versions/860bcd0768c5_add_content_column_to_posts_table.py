"""add content column to posts table

Revision ID: 860bcd0768c5
Revises: 73f610c9920e
Create Date: 2022-05-03 20:54:18.952600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '860bcd0768c5'
down_revision = '73f610c9920e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass

def downgrade():
    op.drop_column('posts', 'content')
    pass