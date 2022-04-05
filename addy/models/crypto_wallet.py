from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relationship
from addy.models.base import Base


class Crypto_wallet(Base):
    __tablename__ = "crypto_wallet"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    balance = Column(Integer, unique=False, nullable=False, server_default="10000")
    transactions = relationship("transactions", backref="crypto_wallet")
    crypto_holdings = relationship("Crypto_holding", back_populates="crypto_wallet")
    user = relationship("User", back_populates="crypto_wallet")
