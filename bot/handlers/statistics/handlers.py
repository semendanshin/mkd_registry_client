from telegram import Update
from telegram.ext import ContextTypes

from crud import user as user_service


async def show_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = await user_service.get_users(context.session)
    users_text = '\n'.join([f'{user.id} - @{user.username} ({user.first_name} - {user.last_name})' for user in users])
    await update.message.reply_text(
        users_text,
    )


async def show_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Здесь будет список заказов',
    )

