"""Attempt to fix fks

Revision ID: 20358e0ceace
Revises: 4d0d2a401d6f
Create Date: 2022-04-05 18:12:13.584011

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20358e0ceace"
down_revision = "4d0d2a401d6f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("crypto_wallet_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "user_wallet_fkey", "user", "crypto_wallet", ["crypto_wallet_id"], ["id"]
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("user_wallet_fkey", "user", type_="foreignkey")
    op.drop_column("user", "crypto_wallet_id")
    # ### end Alembic commands ###
