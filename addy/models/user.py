from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, BigInteger
from sqlalchemy.orm import relationship
from addy.models.base import Base


from addy.models.relationships import user_coin


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    discord_id = Column(BigInteger, unique=True,nullable= True,index = True)
    name = Column(String(255), unique=True, nullable=False)
    favorites = relationship("Coin", secondary=user_coin, back_populates="user")
    
    def __repr__(self) -> str:
        return f"<name={self.name} favorites={self.favorites}>"

    def __str__(self) -> str:
        return f"{self.name} favorites:{self.favorites}"

    def emptyfavorites(self):
        self.favorites = []

    #create a user the necessary required values are present, name discord_id.
    # when empty favorites is called assert that user.favorites is an empty.
