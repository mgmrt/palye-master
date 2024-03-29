"""add finish time in leaflet model

Revision ID: f4166960b2da
Revises: cfcf181b85c0
Create Date: 2021-11-30 19:45:41.523447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4166960b2da'
down_revision = 'cfcf181b85c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('leaflet', sa.Column('finish_time', sa.Time(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('leaflet', 'finish_time')
    # ### end Alembic commands ###
