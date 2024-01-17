from pydantic import BaseModel, ConfigDict, field_validator
from database.enums import ClientTypeEnum
from database.models import User

from typing import Optional

from .user import UserResponse

"""
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
    email:  Mapped[str] = Column(String, nullable=True)

    fio_file_telegram_id:  Mapped[str] = Column(String, nullable=True)
    invoice_file_telegram_id:  Mapped[str] = Column(String, nullable=True)
    r1r7_file_telegram_id:  Mapped[str] = Column(String, nullable=True)

    room_rows_count: Mapped[int] = Column(BigInteger, nullable=True)
    fio_rows_count: Mapped[int] = Column(BigInteger, nullable=True)

    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.CREATED)

    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
"""


class OrderBase(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    egrn_request_id: Optional[int] = None
    address: Optional[str] = None
    cadnum: Optional[str] = None
    contact_phone: Optional[str] = None
    client_type: Optional[ClientTypeEnum] = None
    inn: Optional[str] = None
    company_name: Optional[str] = None
    fio: Optional[str] = None
    email: Optional[str] = None

    fio_file_telegram_id: Optional[str] = None
    invoice_file_telegram_id: Optional[str] = None
    r1r7_file_telegram_id: Optional[str] = None

    room_rows_count: Optional[int] = None
    fio_rows_count: Optional[int] = None

    status: Optional[str] = None

    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class OrderCreate(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    address: str
    cadnum: str
    contact_phone: str
    client_type: ClientTypeEnum
    inn: Optional[str] = None
    company_name: Optional[str] = None
    fio: Optional[str] = None
    email: Optional[str] = None


class OrderResponse(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user: UserResponse
    egrn_request_id: int
    address: str
    cadnum: str
    contact_phone: str
    client_type: ClientTypeEnum

    @field_validator('user', mode='before')
    def validate_user(cls, v, values):
        if isinstance(v, User):
            return UserResponse.model_validate(v)
        return v
