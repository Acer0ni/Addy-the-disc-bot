from sqlalchemy import Column, Table, ForeignKey
from addy.models.base import Base

association_table = Table(
    "association",
    Base.metadata,
    Column("users", ForeignKey("User.id")),
    Column("coin", ForeignKey("Coin.id")),
)
