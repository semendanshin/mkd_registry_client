from .enums import OrderStatusHumanReadableEnum
from database.models import Order
from datetime import datetime
from itertools import groupby


def render_order_preview(order: Order):
    return f"""Заказ #{order.id} - Обновлено: {(datetime.now() - order.updated_at).days} дней назад"""


def render_orders(orders: list[Order]):
    groups = groupby(orders, lambda order: order.status)
    orders_text = '\n\n'.join([f"<b>{OrderStatusHumanReadableEnum.get_human_readable(status)}:</b>\n" +
                               '\n'.join([render_order_preview(order) for order in orders]) for status, orders in
                               groups])
    return orders_text


def render_user(user):
    return (f'{user.created_at.strftime("%d.%m.%Y")}'
            f' - {user.first_name} {user.last_name} (@{user.username})')
