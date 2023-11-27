import pprint

from crud import order as order_service
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.order import OrderCreate
from database.models import Order
from .types import PlaceOrderData
from egrn_requests_api import egrn_requests_api


async def create_order(session: AsyncSession, order: PlaceOrderData) -> Order:
    order_create = OrderCreate(
        user_id=order.user_id,
        egrn_request_id=order.egrn_request_id,
        address=order.address,
        cadnum=order.cadnum,
        contact_phone=order.contact_phone,
        client_type=order.client_type,
        inn=order.inn,
        company_name=order.company_name,
        fio=order.fio,
        fio_file_telegram_id=order.telegram_file_id
    )

    return await order_service.create_order(session, order_create)


async def post_order_to_egrn_api(order: PlaceOrderData) -> PlaceOrderData:
    data = {
        "cadnum": order.cadnum,
        "fio_is_provided": bool(order.telegram_file_id),
    }

    response = await egrn_requests_api.post_request(data)

    order.egrn_request_id = response["id"]

    return order
