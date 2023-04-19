"""empty message

Revision ID: 6b1a6b69aba3
Revises: 24a5520a2370
Create Date: 2023-04-17 11:35:53.128139

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b1a6b69aba3'
down_revision = '24a5520a2370'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('diary', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tags', sa.Text(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('diary', schema=None) as batch_op:
        batch_op.drop_column('tags')

    # ### end Alembic commands ###
