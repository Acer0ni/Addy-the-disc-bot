from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, DateTime, Boolean, Float
from sqlalchemy.sql import func
from addy.models.base import Base
from addy.models.user import User


class Transactions(Base):
    __tablename__ = "Transactions"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    transaction_date = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    coin_id = Column(Integer, ForeignKey("Coin.id"), nullable=False)
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
        return f"({self.transaction_date}) {self.translate_transaction_type()} {self.coin_id} {self.coin_price} {self.amount_transacted} {self.total_price}"

    def __repr__(self):
        return f"<Transaction transaction_time={self.transaction_date} transaction type: {self.translate_transaction_type()} user id:{self.user_id} coin: {self.coin_id} amount: {self.amount_transacted} total price: {self.coin_price}>"
