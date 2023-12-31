"""add new column in User Table

Revision ID: 80263d4031f5
Revises: abd0d397af05
Create Date: 2023-07-02 15:42:29.975417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80263d4031f5'
down_revision = 'abd0d397af05'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('fio', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'fio')
    # ### end Alembic commands ###
