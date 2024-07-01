"""empty message

Revision ID: 505f9b17b236
Revises: 3f973210be2c
Create Date: 2024-06-26 05:03:26.754304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '505f9b17b236'
down_revision = '3f973210be2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('custom_quiz',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.Text(), nullable=False),
    sa.Column('opt1', sa.String(length=100), nullable=False),
    sa.Column('opt2', sa.String(length=100), nullable=False),
    sa.Column('opt3', sa.String(length=100), nullable=False),
    sa.Column('opt4', sa.String(length=100), nullable=False),
    sa.Column('ans', sa.String(length=10), nullable=False),
    sa.Column('pts', sa.Integer(), nullable=False),
    sa.Column('upvote', sa.Integer(), nullable=True),
    sa.Column('downvote', sa.Integer(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('question')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('custom_quiz')
    # ### end Alembic commands ###
