"""populate  coin table

Revision ID: 68b9022bd851
Revises: 97743fcb9a27
Create Date: 2022-03-29 11:04:46.625325

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "68b9022bd851"
down_revision = "97743fcb9a27"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "coin",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("symbol", sa.String(length=255), nullable=True),
        sa.Column("coingecko_id", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("coin")
    # ### end Alembic commands ###
