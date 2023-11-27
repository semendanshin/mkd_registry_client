from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler, CallbackQueryHandler

from bot.handlers.start.keyboards import USERS_KEYBOARD_BUTTON_TEXT, ORDERS_KEYBOARD_BUTTON_TEXT

from . import handlers


def register_handlers(application: Application):
    application.add_handler(
        MessageHandler(
            filters.Text(USERS_KEYBOARD_BUTTON_TEXT),
            handlers.show_users,
        ),
    )

    application.add_handler(
        MessageHandler(
            filters.Text(ORDERS_KEYBOARD_BUTTON_TEXT),
            handlers.show_orders,
        ),
    )
