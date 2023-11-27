from telegram import ReplyKeyboardMarkup, KeyboardButton


ORDER_KEYBOARD_BUTTON_TEXT = 'Заказать'


def get_main_keyboard_for_user() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=ORDER_KEYBOARD_BUTTON_TEXT),
            ],
        ],
        resize_keyboard=True,
    )


USERS_KEYBOARD_BUTTON_TEXT = 'Пользователи🤸🏼'
ORDERS_KEYBOARD_BUTTON_TEXT = 'Заказы🚚'


def get_main_keyboard_for_admin() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=USERS_KEYBOARD_BUTTON_TEXT),
                KeyboardButton(text=ORDERS_KEYBOARD_BUTTON_TEXT),
            ],
        ],
        resize_keyboard=True,
    )
