from telegram.ext import Application, ConversationHandler, CallbackQueryHandler, MessageHandler, filters, CommandHandler

from . import handlers


def register_handlers(app: Application):
    # insert_invoice_
    # show_r1_r7_
    app.add_handler(
          CallbackQueryHandler(
               handlers.send_to_work,
               'to_work_',
          )
    )
    app.add_handler(
        CallbackQueryHandler(
            handlers.admin_cancel_order,
            'cancel_order_',
        )
    )

    app.add_handler(
        ConversationHandler(
            entry_points=[
                CallbackQueryHandler(
                    handlers.start_insert_invoice,
                    'insert_invoice_',
                ),
            ],
            states={
                'INSERT_INVOICE': [
                    MessageHandler(filters.Document.PDF, handlers.insert_invoice),
                ],
            },
            fallbacks=[
                CommandHandler('cancel', handlers.cancel_insert_invoice),
            ],

        )
    )

    app.add_handler(
        CallbackQueryHandler(
            handlers.show_r1_r7,
            'show_r1_r7_',
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            handlers.delete_r1_r7_message,
            'delete_r1r7',
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            handlers.send_reestr_to_production,
            'start_reestr_production',
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            handlers.send_complete_registry_for_email,
            'send_registry_file_to_email_',
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            handlers.send_complete_registry_to_client,
            'send_registry_file_to_tg_',
        )
    )