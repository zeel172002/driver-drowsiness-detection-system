"""Initial migration

Revision ID: 3b0942b3a845
Revises: 
Create Date: 2024-11-18 19:09:11.308457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b0942b3a845'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # Removed op.drop_table('users') since it doesn't exist
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('contact_number', sa.String(length=20), nullable=False, server_default='Unknown'))
        batch_op.add_column(sa.Column('email_id', sa.String(length=100), nullable=False, server_default='unknown@example.com'))
        batch_op.add_column(sa.Column('email_id', sa.String(length=100), nullable=False, server_default='unknown@example.com'))

        batch_op.alter_column('preferred_alert',
            existing_type=sa.VARCHAR(length=100),
            type_=sa.String(length=20),
            existing_nullable=False)
        batch_op.drop_column('experience')
    # ### end Alembic commands ###

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('experience', sa.INTEGER(), nullable=False))
        batch_op.alter_column('preferred_alert',
               existing_type=sa.String(length=20),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.drop_column('email_id')
        batch_op.drop_column('contact_number')

    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('age', sa.INTEGER(), nullable=False),
    sa.Column('experience', sa.INTEGER(), nullable=False),
    sa.Column('preferred_alert', sa.VARCHAR(length=50), nullable=False),
    sa.Column('ear_threshold', sa.FLOAT(), nullable=False),
    sa.Column('blink_count', sa.INTEGER(), nullable=True),
    sa.Column('drowsy_count', sa.INTEGER(), nullable=True),
    sa.Column('ear_changes', sa.VARCHAR(length=200), nullable=True),
    sa.Column('days_active', sa.INTEGER(), nullable=True),
    sa.Column('last_updated', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
