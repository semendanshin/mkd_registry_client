from sqlalchemy import Column, BigInteger, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncAttrs

from datetime import datetime

from .enums import UserRolesEnum, ClientTypeEnum

Base = declarative_base()


class User(AsyncAttrs, Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    username = Column(String, unique=True, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    role = Column(Enum(UserRolesEnum), default=UserRolesEnum.USER)

    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User(id={self.id}, username={self.username}, first_name={self.first_name}, last_name={self.last_name})>'


class Order(Base):
    __tablename__ = 'orders'

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    user_id = Column(BigInteger, ForeignKey('users.id'))
    egrn_request_id = Column(BigInteger, nullable=False)
    address = Column(String, nullable=False)
    cadnum = Column(String, nullable=False)
    contact_phone = Column(String, nullable=False)
    client_type = Column(Enum(ClientTypeEnum), nullable=False)
    inn = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    fio = Column(String, nullable=True)
    fio_file_telegram_id = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)


#
# class Payment(Base):
#     ...

