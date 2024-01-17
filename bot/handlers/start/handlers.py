from telegram import Update
from telegram.ext import ContextTypes

from database.enums import UserRolesEnum

from bot.utils.utils import delete_message_or_skip

from .static_text import WELCOME_MESSAGE, IMPORTANT_MESSAGE
from .keyboards import get_main_keyboard_for_user, get_main_keyboard_for_admin, get_delete_obrazec_keyboard


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # if update.effective_user.first_name:
    #     name = NAME_TEMPLATE.format(
    #         first_name=update.effective_user.first_name,
    #         last_name=update.effective_user.last_name if update.effective_user.last_name else '',
    #     )
    # else:
    #     name = ''

    # text = GREETING_MESSAGE.format(name=name) + '\n' + WELCOME_MESSAGE
    text = WELCOME_MESSAGE

    keyboard = get_main_keyboard_for_admin() if context.database_user.role == UserRolesEnum.ADMIN else (
        get_main_keyboard_for_user())

    await update.effective_message.reply_text(
        text,
        reply_markup=keyboard,
    )

    await update.effective_message.reply_text(
        IMPORTANT_MESSAGE,
    )


async def show_register_sample(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await delete_message_or_skip(update.effective_message)
    with open('data/obrazec.pdf', 'rb') as f:
        await update.effective_message.reply_document(
            document=f,
            filename="Пример заполнения регистрации.pdf",
            reply_markup=get_delete_obrazec_keyboard(),
        )


async def delete_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await delete_message_or_skip(update.effective_message)
