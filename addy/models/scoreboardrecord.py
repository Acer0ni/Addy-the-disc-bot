from ast import For
from enum import unique
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import String, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from addy.models.base import Base


class ScoreboardRecord(Base):
    __tablename__ = "scoreboardrecords"

    _id = Column(Integer, primary_key=True, autoincrement="auto")
    timestamp = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    scoreboard_id = Column(Integer, ForeignKey("scoreboards._id"))
    scoreboard = relationship("Scoreboard", back_populates="records")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User")
    starting_wallet_balance_id = Column(
        Integer, ForeignKey("historical_wallet_values._id")
    )
    ending_wallet_balance_id = Column(
        Integer, ForeignKey("historical_wallet_values._id")
    )
    starting_wallet_balance = relationship(
        "HistoricalWalletValue", foreign_keys=[starting_wallet_balance_id]
    )
    ending_wallet_balance = relationship(
        "HistoricalWalletValue", foreign_keys=[ending_wallet_balance_id]
    )
    score = Column(Float, unique=False, nullable=False)

    def __repr__(self):
        return f"<scoreboardrecord user: {self.user.name} score:{self.score}>"
