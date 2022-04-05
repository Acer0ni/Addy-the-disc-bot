from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from addy.models.base import Base
from sqlalchemy.orm import relationship
from addy.models.relationships import user_coin


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(255), unique=True, nullable=False)
    favorites = relationship("Coin", secondary=user_coin, back_populates="user")
    balance = Column(Integer, unique=False, nullable=False, server_default="10000")
    transactions = relationship("Transactions", backref="user")

    def __repr__(self) -> str:
        return f"<name={self.name} favorites={self.favorites}>"

    def __str__(self) -> str:
        return f"{self.name} favorites:{self.favorites}"

    def emptyfavorites(self):
        self.favorites = []

    def handlebuy(self, amount):
        self.balance = self.balance - amount

    def handlesell(self, amount):
        self.balance = self.balance + amount
