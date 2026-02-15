from bot.db.database import Base
from bot.enums.enums import Statuses, Sender

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, text, ARRAY, BigInteger
from typing import Annotated
from datetime import datetime

intpk = Annotated[int, mapped_column(primary_key=True)]
create_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]

class UsersORM(Base):
    __tablename__ = "users"
    id : Mapped[intpk]
    telegram_id : Mapped[int] = mapped_column(BigInteger, unique=True)
    username : Mapped[str]
    created_at : Mapped[create_at]
    isOnTicket : Mapped[bool]
    
class OperatorsORM(Base):
    __tablename__ = "operators"
    id : Mapped[intpk]
    telegram_id : Mapped[int] = mapped_column(BigInteger, unique=True)
    tickets_id : Mapped[list[int] | None] = mapped_column(ARRAY(Integer))

class TicketsORM(Base):
    __tablename__ = "tickets"
    id : Mapped[intpk]
    user_id : Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"))
    operator_id : Mapped[int | None] = mapped_column(BigInteger, ForeignKey("operators.telegram_id", ondelete="CASCADE"))
    status : Mapped[Statuses]
    created_at : Mapped[create_at]
    messages: Mapped[list["MessagesORM"]] = relationship(
        "MessagesORM",
        back_populates="ticket"
    )
        
class MessagesORM(Base):
    __tablename__ = "messages"
    id : Mapped[intpk]
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id", ondelete="CASCADE"))
    sender : Mapped[Sender]
    text : Mapped[str]
    ticket : Mapped["TicketsORM"] = relationship(
        back_populates= "messages"
    )