from sqlalchemy import Column, BigInteger, String, Enum
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncAttrs


from .enums import UserRolesEnum

Base = declarative_base()


class User(AsyncAttrs, Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    username = Column(String, unique=True, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    role = Column(Enum(UserRolesEnum), default=UserRolesEnum.USER)

    def __repr__(self):
        return f'<User(id={self.id}, username={self.username}, first_name={self.first_name}, last_name={self.last_name})>'


# class Order(Base):
#     ...
#
#
# class Payment(Base):
#     ...

