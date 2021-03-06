from cgitb import text
from sqlalchemy import Column, text
from sqlalchemy.types import Integer, String, Float
from sqlalchemy.orm import relationship
from addy.models.base import Base


class Crypto_wallet(Base):
    __tablename__ = "crypto_wallet"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    # balance needs to be a float
    balance = Column(
        Float,
        unique=False,
        nullable=False,
        default=10_000,
        server_default=text("10000"),
    )
    transactions = relationship("Transaction", back_populates="wallet")
    crypto_holdings = relationship("Crypto_holding", back_populates="crypto_wallet")
    user = relationship("User", back_populates="crypto_wallet")
    historicalvalue = relationship(
        "HistoricalWalletValue", back_populates="crypto_wallet"
    )

    def handle_balance(self, transaction):

        if transaction.is_sale:
            self.balance = self.balance - transaction.total_price
        else:
            self.balance = self.balance + transaction.total_price

    def __str__(self):
        return f"id: {self.id} holdings: {self.crypto_holdings} past values: {self.historicalvalue} balance: {self.balance} "

    def __repr__(self):
        return f"id: {self.id} balance: {self.balance}"
