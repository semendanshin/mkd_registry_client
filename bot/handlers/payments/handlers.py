from telegram import Update
from telegram.ext import CallbackContext

from bot.utils.utils import delete_messages, delete_message_or_skip
from egrn_requests_api import egrn_requests_api
from crud import order as order_service


async def handle_payment(update: Update, context: CallbackContext):
    await update.callback_query.answer()

    order_id = int(update.callback_query.data.split('_')[-1])

    file = await egrn_requests_api.get_request(order_id)

    await update.callback_query.message.reply_document(
        document=file,
        filename=f'Заказ {order_id}.xlsx',
    )

    await delete_message_or_skip(update.callback_query.message)
