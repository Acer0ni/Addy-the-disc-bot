from ast import For
from enum import unique
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import String, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from addy.models.base import Base


class scoreboardRecord(Base):
    __tablename__ = "scoreboardrecords"

    _id = Column(Integer, primary_key=True, autoincrement="auto")
    transaction_date = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    scoreboard_id = Column(Integer, ForeignKey("scoreboards._id"))
    scoreboard = relationship("Scoreboard", back_populates="records")
    name = Column(String(255), unique=True, nullable=False)
    starting_wallet_balance = Column(Float, unique=False, nullable=False)
    ending_wallet_balance = Column(Float, unique=False, nullable=False)
    score = Column(Float, unique=False, nullable=False)
