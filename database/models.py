from sqlalchemy import Column, BigInteger, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, Mapped, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs

from datetime import datetime

from .enums import UserRolesEnum, ClientTypeEnum, OrderStatusEnum


Base = declarative_base()


class User(AsyncAttrs, Base):
    __tablename__ = 'users'

    id: Mapped[int] = Column(BigInteger, primary_key=True)
    username: Mapped[str] = Column(String, unique=True, nullable=True)
    first_name: Mapped[str] = Column(String, nullable=True)
    last_name: Mapped[str] = Column(String, nullable=True)
    role: Mapped[UserRolesEnum] = Column(Enum(UserRolesEnum), default=UserRolesEnum.USER)

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")

    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User(id={self.id}, username={self.username}, first_name={self.first_name}, last_name={self.last_name})>'


class Order(Base):
    __tablename__ = 'orders'

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    user_id:  Mapped[int] = Column(BigInteger, ForeignKey('users.id'))
    egrn_request_id:  Mapped[int] = Column(BigInteger, nullable=True)
    address:  Mapped[str] = Column(String, nullable=False)
    cadnum:  Mapped[str] = Column(String, nullable=False)
    contact_phone:  Mapped[str] = Column(String, nullable=False)
    client_type:  Mapped[ClientTypeEnum] = Column(Enum(ClientTypeEnum), nullable=False)
    inn:  Mapped[str] = Column(String, nullable=True)
    company_name:  Mapped[str] = Column(String, nullable=True)
    fio:  Mapped[str] = Column(String, nullable=True)

    fio_file_telegram_id:  Mapped[str] = Column(String, nullable=True)
    invoice_file_telegram_id:  Mapped[str] = Column(String, nullable=True)
    r1r7_file_telegram_id:  Mapped[str] = Column(String, nullable=True)

    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.CREATED)

    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="orders")


#
# class Payment(Base):
#     ...

