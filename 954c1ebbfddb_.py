"""empty message

Revision ID: 954c1ebbfddb
Revises: 
Create Date: 2024-11-18 21:33:49.769853

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '954c1ebbfddb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('contact_number', sa.String(length=20), nullable=False),
    sa.Column('email_id', sa.String(length=100), nullable=False),
    sa.Column('preferred_alert', sa.String(length=20), nullable=False),
    sa.Column('ear_threshold', sa.Float(), nullable=False),
    sa.Column('blink_count', sa.Integer(), nullable=True),
    sa.Column('drowsy_count', sa.Integer(), nullable=True),
    sa.Column('ear_changes', sa.Integer(), nullable=True),
    sa.Column('days_active', sa.Integer(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
