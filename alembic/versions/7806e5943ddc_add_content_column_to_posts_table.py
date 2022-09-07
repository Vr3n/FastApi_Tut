"""add content column to posts table

Revision ID: 7806e5943ddc
Revises: cc91dcad2c6b
Create Date: 2022-09-07 19:02:46.462923

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7806e5943ddc'
down_revision = 'cc91dcad2c6b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
