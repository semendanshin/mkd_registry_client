from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_confirm_keyboard(callback_pattern_start: str) -> InlineKeyboardMarkup:
    """
    Example:
    callback_pattern_start = 'confirm'
    row_width = 2
    result:
    [
        [
            InlineKeyboardButton('Да', callback_data='confirm_1'),
            InlineKeyboardButton('Нет', callback_data='confirm_0'),
        ],
    ]

    :param callback_pattern_start:
    :param row_width:
    :return:
    """
    keyboard = [
        [
            InlineKeyboardButton('Нет', callback_data=f'{callback_pattern_start}_0'),
            InlineKeyboardButton('Да', callback_data=f'{callback_pattern_start}_1'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_delete_message_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('Удалить', callback_data='delete_message'),
            ],
        ]
    )
