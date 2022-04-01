from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from addy.models.base import Base
from sqlalchemy.orm import relationship
from addy.models.relationships import association_table


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(255), unique=True, nullable=False)
    favorites = relationship("Coin", secondary=association_table, back_populates="user")

    def __repr__(self) -> str:
        return f"<name={self.name} favorites={self.favorites}>"

    def __str__(self) -> str:
        return f"{self.name} favorites:{self.favorites}"

    def emptyfavorites(self):
        self.favorites = []
