from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext import Application

from . import handlers


def register_handlers(app: Application):
    app.add_handler(
        CommandHandler('start', handlers.start),
    )
    app.add_handler(
        CommandHandler('obrazec', handlers.show_register_sample),
    )
    app.add_handler(
        CallbackQueryHandler(
            handlers.delete_message,
            'delete_obrazec',
        )
    )
    app.add_handler(
        CallbackQueryHandler(
            handlers.delete_message,
            'delete_message',
        )
    )
