"""event table

Revision ID: 5a7bbc9cb7a3
Revises: 94f6b4d83de1
Create Date: 2019-10-15 00:06:01.927665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a7bbc9cb7a3'
down_revision = '94f6b4d83de1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('address', sa.String(length=256), nullable=True),
    sa.Column('img_url', sa.String(length=256), nullable=True),
    sa.Column('event_url', sa.String(length=256), nullable=True),
    sa.Column('distance', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_event_address'), 'event', ['address'], unique=False)
    op.create_index(op.f('ix_event_distance'), 'event', ['distance'], unique=False)
    op.create_index(op.f('ix_event_event_url'), 'event', ['event_url'], unique=False)
    op.create_index(op.f('ix_event_img_url'), 'event', ['img_url'], unique=False)
    op.create_index(op.f('ix_event_name'), 'event', ['name'], unique=False)
    op.create_index(op.f('ix_event_rating'), 'event', ['rating'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_event_rating'), table_name='event')
    op.drop_index(op.f('ix_event_name'), table_name='event')
    op.drop_index(op.f('ix_event_img_url'), table_name='event')
    op.drop_index(op.f('ix_event_event_url'), table_name='event')
    op.drop_index(op.f('ix_event_distance'), table_name='event')
    op.drop_index(op.f('ix_event_address'), table_name='event')
    op.drop_table('event')
    # ### end Alembic commands ###
