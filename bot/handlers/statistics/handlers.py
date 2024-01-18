from telegram import Update
from telegram.ext import ContextTypes

from crud import user as user_service
from crud import order as order_service

from database.enums import OrderStatusEnum, UserRolesEnum

from bot.handlers.place_order.manage_data import get_order_card_text_from_orm
from bot.utils.keyboards import get_delete_message_keyboard

from .manage_data import render_orders

import logging

logger = logging.getLogger(__name__)


async def show_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = await user_service.get_non_clients(context.session)
    users_text = '\n'.join([f'{user.created_at} - {user.first_name} {user.last_name} (@{user.username})' for user in users])
    await update.message.reply_text(
        users_text,
    )


async def show_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    statuses_to_show = [
        OrderStatusEnum.INWORK,
        OrderStatusEnum.R1R7DONE,
        OrderStatusEnum.INVOICESENT,
        OrderStatusEnum.INVOICEPAID,
        OrderStatusEnum.REGISTRYINWORK,
    ]

    orders = await order_service.get_orders_by_statuses(context.session, statuses_to_show)

    orders_text = render_orders(orders)

    await update.message.reply_text(
        orders_text,
    )


async def show_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.database_user.role != UserRolesEnum.ADMIN:
        await update.message.reply_text(
            "У вас нет прав для выполнения этой команды.",
        )
        return

    if not context.args:
        await update.message.reply_text(
            "Не указан номер заказа.",
        )
        return

    try:
        order_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text(
            "Неверный формат аргумента. Ожидается число.",
        )
        return

    order = await order_service.get_order(context.session, order_id)

    if not order:
        await update.message.reply_text(
            f"Заказ #{order_id} не найден.",
        )
        return

    text = await get_order_card_text_from_orm(context.session, order)

    await update.message.reply_text(
        text,
        reply_markup=get_delete_message_keyboard(),
    )


async def show_clients(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clients = await user_service.get_clients(context.session)
    clients_text = '\n'.join([f'{client.created_at} - {client.first_name} {client.last_name} (@{client.username})' for client in clients])
    await update.message.reply_text(
        clients_text,
    )
