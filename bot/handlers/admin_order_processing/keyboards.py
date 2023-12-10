from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_delete_r1r7_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('Удалить', callback_data='delete_r1r7'),
            ],
        ]
    )


def get_paid_keyboard(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('Оплачено', callback_data=f'paid_{order_id}'),
            ],
        ]
    )