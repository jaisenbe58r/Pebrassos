"""Model hist slug

Revision ID: 5fb42db5d526
Revises: 179350e18f71
Create Date: 2020-10-05 18:10:46.739002

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fb42db5d526'
down_revision = '179350e18f71'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hist_weather_statiion', sa.Column('Location_name_slug', sa.String(length=80), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('hist_weather_statiion', 'Location_name_slug')
    # ### end Alembic commands ###