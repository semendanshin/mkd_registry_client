from telegram.ext import Application, CallbackQueryHandler

from .handlers import handle_payment


def register_handlers(application: Application):
    application.add_handler(
        CallbackQueryHandler(
            handle_payment,
            'paid_*',
        ),
    )
