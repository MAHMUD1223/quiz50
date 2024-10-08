"""empty message

Revision ID: b917e91ecba0
Revises: 
Create Date: 2024-06-23 01:45:01.558988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b917e91ecba0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('point', sa.Integer(), nullable=True),
    sa.Column('current_q', sa.Integer(), nullable=True),
    sa.Column('current_qset', sa.Integer(), nullable=True),
    sa.Column('done_qset', sa.String(length=50), nullable=True),
    sa.Column('_password', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
