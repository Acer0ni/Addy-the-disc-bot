"""changed scboard records name

Revision ID: 7b35b66dc6b1
Revises: d84984014d00
Create Date: 2022-04-11 17:32:40.962710

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7b35b66dc6b1'
down_revision = 'd84984014d00'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scoreboardrecords', sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.drop_column('scoreboardrecords', 'transaction_date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scoreboardrecords', sa.Column('transaction_date', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.drop_column('scoreboardrecords', 'timestamp')
    # ### end Alembic commands ###
