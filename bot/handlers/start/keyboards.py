from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


ORDER_KEYBOARD_BUTTON_TEXT = 'Заказать реестр'


def get_main_keyboard_for_user() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=ORDER_KEYBOARD_BUTTON_TEXT),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
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


def get_delete_obrazec_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Удалить образец', callback_data='delete_obrazec'),
            ],
        ],
    )
