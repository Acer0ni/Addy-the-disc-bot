from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, Float
from sqlalchemy.orm import relationship
from addy.models.base import Base


class Crypto_holding(Base):
    __tablename__ = "crypto_holdings"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(255), unique=False, nullable=False)
    coingecko_id = Column(String(255), unique=False, nullable=False)
    amount = Column(Float, nullable=False)
    crypto_wallet_id = Column(Integer, ForeignKey("crypto_wallet.id"))
    crypto_wallet = relationship("Crypto_wallet", back_populates="crypto_holdings")
