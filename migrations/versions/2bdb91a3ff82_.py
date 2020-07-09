"""empty message

Revision ID: 2bdb91a3ff82
Revises: 4e6e6b4cae0d
Create Date: 2020-07-09 14:50:45.050896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bdb91a3ff82'
down_revision = '4e6e6b4cae0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=200), nullable=True))
    op.drop_column('user', 'abot_me')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('abot_me', sa.VARCHAR(length=200), nullable=True))
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###