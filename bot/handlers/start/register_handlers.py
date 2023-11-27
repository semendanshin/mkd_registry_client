from telegram.ext import CommandHandler
from telegram.ext import Application

from . import handlers


def register_handlers(app: Application):
    app.add_handler(
        CommandHandler('start', handlers.start),
    )
    app.add_handler(
        CommandHandler('obrazec', handlers.show_register_sample),
    )
