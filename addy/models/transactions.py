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
    coin_price_at_time_of_transaction = Column(Float, nullable=False)
