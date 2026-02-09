from db.database import async_engine, session_factory, Base
from enums.enums import Statuses, Sender

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, MetaData, ForeignKey, Column, text, BigInteger
from typing import Annotated
from datetime import datetime
from enum import Enum

intpk = Annotated[int, mapped_column(primary_key=True)]
create_at = Annotated[datetime, mapped_column(server_default=text("TIMEZOE('utc', now())"))]

class UsersORM(Base):
    __tablename__ = "users"
    id : Mapped[intpk]
    telegram_id : Mapped[BigInteger] = mapped_column(unique=True)
    username : Mapped[str]
    created_at : Mapped[create_at]
    
class OperatorsORM(Base):
    __tablename__ = "operators"
    id : Mapped[intpk]
    telegram_id : Mapped[BigInteger] = mapped_column(unique=True)
    tickets_id : Mapped[list[int] | None]

class TicketsORM(Base):
    __tablename__ = "tickets"
    id : Mapped[intpk]
    user_id : Mapped[BigInteger] = mapped_column(ForeignKey("users.telegram_id", ondelete="CASCADE"))
    operator_id : Mapped[BigInteger | None] = mapped_column(ForeignKey("operators.telegram_id", ondelete="CASCADE"))
    status : Mapped[Statuses]
    created_at : Mapped[create_at]
    messages : Mapped[list["MessagesORM"] | None] = relationship(
        back_populates= "ticket"
    )
        
class MessagesORM(Base):
    __tablename__ = "messages"
    id : Mapped[intpk]
    ticket : Mapped["TicketsORM"] = relationship(
        back_populates= "messages"
    )
    sender : Mapped[Sender]
    text : Mapped[str]