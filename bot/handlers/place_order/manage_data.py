import pprint

from crud import order as order_service
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.order import OrderCreate
from database.models import Order
from .types import PlaceOrderData, ClientTypeEnum
from egrn_requests_api import egrn_requests_api
from .static_text import ORDER_TEMPLATE, LEGAL_ORDER_INFO_TEMPLATE, INDIVIDUAL_ORDER_INFO_TEMPLATE


async def create_order(session: AsyncSession, order: PlaceOrderData) -> Order:
    order_create = OrderCreate(
        user_id=order.user_id,
        # egrn_request_id=order.egrn_request_id,
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


def get_order_card_text(data: PlaceOrderData | Order, order_id: int = -1) -> str:
    return ORDER_TEMPLATE.format(
        order_number_text=f"Заказ #{order_id}\n" if order_id != -1 else "",
        fio_is_provided_text="c ФИО" if data.telegram_file_id else "без ФИО",
        cadnum=data.cadnum,
        address=data.address,
        username=data.username or "(У пользователя нет username)",
        first_name=data.first_name,
        phone=data.contact_phone,
        email=data.email,
        customer_info=LEGAL_ORDER_INFO_TEMPLATE.format(
            org_name=data.company_name,
            inn=data.inn,
        ) if data.client_type == ClientTypeEnum.LEGAL else INDIVIDUAL_ORDER_INFO_TEMPLATE.format(
            fio=data.fio,
        ),
        filename=data.filename if data.filename else "",
    )


async def get_order_card_text_from_orm(session: AsyncSession, order: Order):
    await session.refresh(order, ["user"])

    data = PlaceOrderData(
        user_id=order.user_id,
        username=order.user.username,
        first_name=order.user.first_name,
        last_name=order.user.last_name,
        address=order.address,
        cadnum=order.cadnum,
        contact_phone=order.contact_phone,
        email=order.email,
        client_type=order.client_type,
        inn=order.inn,
        company_name=order.company_name,
        fio=order.fio,
        telegram_file_id=order.fio_file_telegram_id,
    )

    return get_order_card_text(data, order_id=order.id)
