"""empty message

Revision ID: 6fd085268f00
Revises: 089ac06935df
Create Date: 2018-12-30 19:07:44.459923

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fd085268f00'
down_revision = '089ac06935df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('verified', sa.Boolean(), nullable=True))
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'verified')
    # ### end Alembic commands ###