from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String
from addy.models.base import Base
from addy.models.relationships import user_coin


class Coin(Base):
    __tablename__ = "coin"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(255), unique=False, nullable=False)
    symbol = Column(String(255), unique=False, nullable=False)
    coingecko_id = Column(String(255), unique=False, nullable=False)
    user = relationship("User", secondary=user_coin, back_populates="favorites")
    transactions = relationship("Transaction", backref="coin")

    def __repr__(self) -> str:
        return f"<Coin name={self.name} symbol={self.symbol}>"

    def __str__(self) -> str:
        return self.name
