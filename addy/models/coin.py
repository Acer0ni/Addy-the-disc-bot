from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String
from addy.models.base import Base
from addy.models.relationships import association_table


class Coin(Base):
    __tablename__ = "Coin"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(255), unique=False, nullable=True)
    symbol = Column(String(255), unique=False, nullable=True)
    coingecko_id = Column(String(255), unique=False, nullable=True)
    user = relationship("User", secondary=association_table, back_populates="favorites")

    def __repr__(self) -> str:
        return f"<Coin name={self.name} symbol={self.symbol}>"

    def __str__(self) -> str:
        return self.name
