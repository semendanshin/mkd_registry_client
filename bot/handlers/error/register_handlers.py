from telegram.ext import Application, CallbackQueryHandler

from .handlers import send_stacktrace_to_tg_chat


def register_handlers(application: Application):
    application.add_error_handler(send_stacktrace_to_tg_chat)
