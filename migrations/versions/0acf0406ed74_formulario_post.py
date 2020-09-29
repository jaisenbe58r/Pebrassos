"""Formulario Post

Revision ID: 0acf0406ed74
Revises: 41bf32d56f87
Create Date: 2020-09-29 23:27:31.342899

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0acf0406ed74'
down_revision = '41bf32d56f87'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('date', sa.DateTime(), nullable=True))
    op.add_column('post', sa.Column('loc', sa.Text(), nullable=True))
    op.add_column('post', sa.Column('state', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'state')
    op.drop_column('post', 'loc')
    op.drop_column('post', 'date')
    # ### end Alembic commands ###
