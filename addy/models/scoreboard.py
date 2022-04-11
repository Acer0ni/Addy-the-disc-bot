from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String, Float, DateTime
from sqlalchemy.sql import func
from addy.models.base import Base


class Scoreboard(Base):
    __tablename__ = "scoreboards"

    _id = Column(Integer, primary_key=True, autoincrement="auto")
    timestamp = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    records = relationship("scoreboardRecord", back_populates="scoreboard")
