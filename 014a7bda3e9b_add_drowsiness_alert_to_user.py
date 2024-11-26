"""Add drowsiness_alert to User

Revision ID: 014a7bda3e9b
Revises: 954c1ebbfddb
Create Date: 2024-11-18 22:10:04.740513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '014a7bda3e9b'
down_revision = '954c1ebbfddb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('drowsiness_alert', sa.String(length=120), nullable=True))
        batch_op.alter_column('ear_changes',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=200),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('ear_changes',
               existing_type=sa.String(length=200),
               type_=sa.INTEGER(),
               existing_nullable=True)
        batch_op.drop_column('drowsiness_alert')

    # ### end Alembic commands ###