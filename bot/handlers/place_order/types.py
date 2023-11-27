from pydantic import BaseModel
from database.enums import ClientTypeEnum


class PlaceOrderData(BaseModel):
    user_id: int = None
    username: str = None
    first_name: str = None

    egrn_request_id: int = None

    address: str = None
    cadnum: str = None

    contact_phone: str = None

    client_type: ClientTypeEnum = None
    inn: str = None
    company_name: str = None
    fio: str = None

    filename: str = None
    telegram_file_id: str = None
