from telegram.ext import Application
from telegram.ext import ConversationHandler, MessageHandler, CallbackQueryHandler, filters, CommandHandler

from .enums import PlaceOrderConversationSteps
from .handlers import *
from bot.handlers.start.keyboards import ORDER_KEYBOARD_BUTTON_TEXT


def register_handlers(app: Application):
    handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Text((ORDER_KEYBOARD_BUTTON_TEXT, )), start_place_order),
        ],
        states={
            PlaceOrderConversationSteps.ADDRESS_OR_CADNUMBER: [
                MessageHandler(filters.Regex(r"\d+:\d+"), process_cadnum),
                MessageHandler(filters.Text() & ~filters.Command(), process_address),
            ],
            PlaceOrderConversationSteps.CONFIRM_ADDRESS: [
                CallbackQueryHandler(confirm_address, pattern=r"^place_order_confirm_address_(1|0)$"),
            ],
            PlaceOrderConversationSteps.CONTACT_PHONE: [
                MessageHandler(filters.Text() & ~filters.Command(), process_contact_phone),
            ],
            PlaceOrderConversationSteps.CONFIRM_PHONE: [
                CallbackQueryHandler(confirm_contact_phone, pattern=r"^place_order_confirm_contact_phone_(1|0)$"),
            ],
            PlaceOrderConversationSteps.CHOOSE_CLIENT_TYPE: [
                CallbackQueryHandler(process_client_type, pattern=r"^place_order_client_type_"),
            ],
            PlaceOrderConversationSteps.ADD_INN: [
                MessageHandler(filters.Text() & ~filters.Command(), process_inn),
            ],
            PlaceOrderConversationSteps.ADD_FIO: [
                MessageHandler(filters.Text() & ~filters.Command(), process_fio),
            ],
            PlaceOrderConversationSteps.CONFIRM_INN_OR_FIO: [
                CallbackQueryHandler(confirm_fio_or_inn, pattern=r"^place_order_confirm_fio_or_inn_(1|0)$"),
            ],
            PlaceOrderConversationSteps.ADD_FIO_FILE: [
                MessageHandler(filters.Document.ALL, process_fio_file),
                CommandHandler("0", show_order_confirmation),
            ],
            PlaceOrderConversationSteps.CONFIRM_ORDER: [
                CallbackQueryHandler(confirm_order, pattern=r"^place_order_confirm_order_(1|0)$"),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel_place_order),
            CallbackQueryHandler(cancel_place_order, pattern=r"^cancel^"),
        ],
        name="place_order",
        persistent=True,
    )

    app.add_handler(handler)
