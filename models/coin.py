from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, Text, String

Base = declarative_base


class Coin(Base):
    __tablename__ = "coin"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    coin_name = Column(String(255), unique=False, nullable=True)
    symbol = Column(String(255), unique=False, nullable=True)
    coin_id = Column(String(255), unique=False, nullable=True)
