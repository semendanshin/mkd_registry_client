from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from bot.handlers.place_order.manage_data import get_order_card_text_from_orm
from bot.utils.utils import delete_messages, delete_message_or_skip
from database.enums import OrderStatusEnum
from egrn_requests_api import egrn_requests_api

from crud import user as user_service
from crud import order as order_service


async def handle_payment(update: Update, context: CallbackContext):
    order_id = int(update.callback_query.data.split('_')[-1])

    order = await order_service.get_order(context.session, order_id)

    admins = await user_service.get_admins(context.session)
    admin = admins[0] if admins else None

    if not admin:
        raise RuntimeError("Admin not found")

    text = "Подтвердите оплату заказа\n\n"
    text += await get_order_card_text_from_orm(context.session, order)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Отправить в работу", callback_data=f"start_reestr_production_{order.id}"),
            ]
        ]
    )

    await context.bot.send_message(
        chat_id=admin.id,
        text=text,
        reply_markup=keyboard,
    )

    await update.callback_query.answer(
        text="Отправлено в работу",
        show_alert=True,
    )

    await order_service.update_order(context.session, order_id, status=OrderStatusEnum.REGISTRYINWORK)

    await delete_messages(context)
    await delete_message_or_skip(update.callback_query.message)
