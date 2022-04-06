from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, DateTime, Boolean, Float
from sqlalchemy.sql import func
from addy.models.base import Base


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    transaction_date = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    wallet_id = Column(Integer, ForeignKey("crypto_wallet.id"), nullable=False)
    wallet = relationship("Crypto_wallet", back_populates="transactions")
    coin_id = Column(Integer, ForeignKey("coin.id"), nullable=False)
    transaction_type = Column(Boolean, nullable=False)
    amount_transacted = Column(Float, nullable=False)
    coin_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total_price = self.amount_transacted * self.coin_price

    def translate_transaction_type(self):
        return "BUY" if self.transaction_type else "SELL"

    def __str__(self):
        return f"time: {self.transaction_date} type:{self.transaction_type} amount: {self.amount_transacted} coin price: {self.coin_price} total: {self.total_price}"

    def __repr__(self):
        return f"<Transaction transaction_time={self.transaction_date} transaction type: {self.translate_transaction_type()} coin price: {self.coin_price} amount: {self.amount_transacted} total price: {self.total_price}>"
