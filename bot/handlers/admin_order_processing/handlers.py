from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.utils.utils import delete_message_or_skip, delete_messages

from crud import order as order_service
from egrn_requests_api import egrn_requests_api

from database.enums import OrderStatusEnum

from .keyboards import get_delete_r1r7_keyboard, get_paid_keyboard


async def send_to_work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    order_id = int(update.callback_query.data.split('_')[-1])

    order = await order_service.get_order(context.session, order_id)

    order_request = await egrn_requests_api.create_request(order.cadnum, bool(order.fio_file_telegram_id), order.id)
    order_request_id = order_request.get("id")

    await order_service.update_order(context.session, order_id, egrn_request_id=order_request_id, status=OrderStatusEnum.INWORK)

    await update.callback_query.answer(
        text="Заказ отправлен на обработку",
        show_alert=True,
    )

    await delete_message_or_skip(update.callback_query.message)

    return ConversationHandler.END


async def admin_cancel_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    order_id = int(update.callback_query.data.split('_')[-1])

    await update.callback_query.answer(
        text="Заказ отменен",
        show_alert=True,
    )

    await delete_message_or_skip(update.callback_query.message)

    return ConversationHandler.END


async def start_insert_invoice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    order_id = int(update.callback_query.data.split('_')[-1])

    context.user_data["order_id"] = order_id
    context.user_data["effective_message"] = update.effective_message

    message = await update.effective_message.reply_text(
        text="Отправьте счет в формате .pdf",
    )

    context.user_data["messages_to_delete"] = [message]

    return 'INSERT_INVOICE'


async def insert_invoice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    order_id = context.user_data["order_id"]

    file_id = update.message.document.file_id

    await order_service.update_order(context.session, order_id, invoice_file_telegram_id=file_id)

    order = await order_service.get_order(context.session, order_id)

    await context.bot.send_document(
        chat_id=order.user_id,
        caption=f"Оплатите заказ номер {order.id}",
        document=file_id,
        reply_markup=get_paid_keyboard(order.id),
    )

    await update.message.reply_text(
        text="Счет успешно добавлен",
    )

    await delete_message_or_skip(update.message)
    await delete_message_or_skip(context.user_data.get("effective_message"))

    await delete_messages(context)

    del context.user_data["order_id"]

    return ConversationHandler.END


async def show_r1_r7(update: Update, context: ContextTypes.DEFAULT_TYPE):
    order_id = int(update.callback_query.data.split('_')[-1])

    order = await order_service.get_order(context.session, order_id)

    r1r7_file = await egrn_requests_api.get_r1r7_file(order.egrn_request_id)

    filename = f"r1r7_{order.id}_{order.cadnum}.xlsx"

    await update.callback_query.message.reply_document(
        document=r1r7_file,
        filename=filename,
        reply_markup=get_delete_r1r7_keyboard(),
    )

    return ConversationHandler.END


async def delete_r1_r7_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await delete_message_or_skip(update.callback_query.message)
    await update.callback_query.answer()
    return ConversationHandler.END


async def cancel_insert_invoice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text="Отмена",
    )

    await delete_messages(context)
    await delete_message_or_skip(update.message)

    return ConversationHandler.END


async def send_reestr_to_production(update: Update, context: ContextTypes.DEFAULT_TYPE):
    order_id = int(update.callback_query.data.split('_')[-1])

    order = await order_service.get_order(context.session, order_id)

    await egrn_requests_api.reestr_to_production(order.egrn_request_id)

    await update.callback_query.answer(
        text="Реестр отправлен в производство",
        show_alert=True,
    )

    await delete_message_or_skip(update.effective_message)

    return ConversationHandler.END
