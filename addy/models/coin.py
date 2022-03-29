from sqlalchemy import Column
from sqlalchemy.types import Integer, Text, String
from addy.models.base import Base


class Coin(Base):
    __tablename__ = "coin"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(255), unique=False, nullable=True)
    symbol = Column(String(255), unique=False, nullable=True)
    coingecko_id = Column(String(255), unique=False, nullable=True)
