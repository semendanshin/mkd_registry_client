from typing import Optional

from pydantic import BaseModel
from database.enums import ClientTypeEnum


class PlaceOrderData(BaseModel):
    user_id: int = None
    username: Optional[str] = None
    first_name: str = None

    egrn_request_id: int = None

    address: str = None
    cadnum: str = None

    contact_phone: str = None

    client_type: ClientTypeEnum = None
    inn: Optional[str] = None
    company_name: Optional[str] = None
    fio: Optional[str] = None

    filename: Optional[str] = None
    telegram_file_id: Optional[str] = None
