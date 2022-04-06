"""i hope this works

Revision ID: bc73cb377f55
Revises: 0fcd31033c41
Create Date: 2022-04-05 15:33:05.565002

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "bc73cb377f55"
down_revision = "0fcd31033c41"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.rename_table("Coin", "coin")
    op.execute('ALTER SEQUENCE "Coin_id_seq" RENAME TO coin_id_seq')
    op.execute('ALTER INDEX "Coin_pkey" RENAME TO coin_pkey')
    op.rename_table("User", "user")
    op.execute('ALTER SEQUENCE "User_id_seq" RENAME TO user_id_seq')
    op.execute('ALTER INDEX "User_pkey" RENAME TO user_pkey')
    op.rename_table("Transactions", "transaction")
    op.execute('ALTER SEQUENCE "Transactions_id_seq" RENAME TO transaction_id_seq')
    op.execute('ALTER INDEX "Transactions_pkey" RENAME TO transaction_pkey')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.rename_table("coin", "Coin")
    op.execute('ALTER SEQUENCE coin_id_seq RENAME TO "Coin_id_seq"')
    op.execute('ALTER INDEX coin_pkey RENAME TO "Coin_pkey"')
    op.rename_table("user", "User")
    op.execute('ALTER SEQUENCE user_id_seq RENAME TO "User_id_seq"')
    op.execute('ALTER INDEX user_pkey RENAME TO "User_pkey"')
    op.rename_table("transaction", "Transaction")
    op.execute('ALTER SEQUENCE transaction_id_seq RENAME TO "Transactions_id_seq"')
    op.execute('ALTER INDEX transaction_pkey RENAME TO "Transactions_pkey"')
    # ### end Alembic commands ###