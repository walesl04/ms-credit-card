"""update ocupation user.

Revision ID: b35369786350
Revises: 860e4c923841
Create Date: 2023-09-09 14:00:24.854545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b35369786350'
down_revision = '860e4c923841'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('ocupation',
               existing_type=sa.VARCHAR(length=200),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('ocupation',
               existing_type=sa.VARCHAR(length=200),
               nullable=False)

    # ### end Alembic commands ###
