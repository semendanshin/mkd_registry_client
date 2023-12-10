from pydantic import BaseModel, ConfigDict, field_validator
from database.enums import ClientTypeEnum
from database.models import User

from typing import Optional

from .user import UserResponse

"""
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
"""


class OrderBase(BaseModel):
    user_id: Optional[int] = None
    egrn_request_id: Optional[int] = None
    address: Optional[str] = None
    cadnum: Optional[str] = None
    contact_phone: Optional[str] = None
    client_type: Optional[ClientTypeEnum] = None
    inn: Optional[str] = None
    company_name: Optional[str] = None
    fio: Optional[str] = None
    fio_file_telegram_id: Optional[str] = None


class OrderCreate(OrderBase):
    user_id: int
    egrn_request_id: Optional[int] = None
    address: str
    cadnum: str
    contact_phone: str
    client_type: ClientTypeEnum
    inn: Optional[str] = None
    company_name: Optional[str] = None
    fio: Optional[str] = None
    fio_file_telegram_id: Optional[str] = None


class OrderResponse(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user: UserResponse
    egrn_request_id: int
    address: str
    cadnum: str
    contact_phone: str
    client_type: ClientTypeEnum
    inn: Optional[str] = None
    company_name: Optional[str] = None
    fio: Optional[str] = None
    fio_file_telegram_id: Optional[str] = None

    @field_validator('user', mode='before')
    def validate_user(cls, v, values):
        if isinstance(v, User):
            return UserResponse.model_validate(v)
        return v
