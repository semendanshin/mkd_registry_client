from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot
from egrn_requests_api import egrn_requests_api
from bot.handlers.place_order.manage_data import get_order_card_text_from_orm
from database.enums import OrderStatusEnum

from sqlalchemy.ext.asyncio import AsyncSession

from crud import user as user_service
from crud import order as order_service

from bot import telegram_app


async def send_r1r7_to_admin(session: AsyncSession, order_id: int):
    order = await order_service.get_order(session, order_id)

    if not order:
        raise AttributeError("Order not found")

    bot: Bot = telegram_app.bot

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Выставить счет", callback_data=f"insert_invoice_{order.id}"),
            ]
        ]
    )

    admins = await user_service.get_admins(session)
    admin = admins[0] if admins else None

    if not admin:
        raise RuntimeError("Admin not found")

    text = (f"Р1Р7 готов\n\n"
            f"Количество помещений: {order.room_rows_count}\n"
            f"Количество собственников: {order.fio_rows_count}\n\n")
    text += await get_order_card_text_from_orm(session, order)

    await bot.send_message(
        chat_id=admin.id,
        text=text,
        reply_markup=keyboard,
    )

    await order_service.update_order(session, order_id, status=OrderStatusEnum.R1R7DONE)


async def send_registry_file_to_admin(session: AsyncSession, order_id):
    order = await order_service.get_order(session, order_id)

    if not order:
        raise AttributeError("Order not found")

    bot: Bot = telegram_app.bot

    admins = await user_service.get_admins(session)
    admin = admins[0] if admins else None

    if not admin:
        raise RuntimeError("Admin not found")

    text = (f"Заказ готов\n\n"
            f"КВ+НЖ+ММ = {round(order.total_area, 2)} м2")
    text += await get_order_card_text_from_orm(session, order)

    # file_bytes = await egrn_requests_api.get_registry_file(order.egrn_request_id)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Для email", callback_data=f"send_registry_file_to_email_{order.id}"),
            ],
            [
                InlineKeyboardButton(text="Отправить в тг", callback_data=f"send_registry_file_to_tg_{order.id}"),
            ],
        ]
    )

    await bot.send_message(
        chat_id=admin.id,
        text=text,
        reply_markup=keyboard,
    )

    # await bot.send_document(
    #     chat_id=admin.id,
    #     document=file_bytes,
    #     filename=f"{order.id}_реестр.xlsx",
    # )

    await order_service.update_order(session, order_id, status=OrderStatusEnum.DONE)
