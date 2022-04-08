from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, Float, DateTime
from sqlalchemy.sql import func
from addy.models.base import Base


class HistoricalWalletValue(Base):
    __tablename__ = "historical_wallet_values"

    _id = Column(Integer, primary_key=True, autoincrement="auto")
    crypto_wallet_id = Column(Integer, ForeignKey("crypto_wallet.id"), nullable=False)
    timestamp = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    usd_balance = Column(Float, nullable=False)
    holdings_balance = Column(Float, nullable=False)
    total_balance = Column(Float, nullable=False)
    crypto_wallet = relationship("Crypto_wallet", back_populates="historicalvalue")
