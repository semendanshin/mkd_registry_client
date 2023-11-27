from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot.utils.keyboards import get_confirm_keyboard
from .enums import ClientTypeHumanReadable


CONFIRM_ADDRESS_PATTERN = 'place_order_confirm_address'


def get_confirm_address_keyboard() -> InlineKeyboardMarkup:
    return get_confirm_keyboard(
        callback_pattern_start=CONFIRM_ADDRESS_PATTERN,
    )


CONFIRM_CONTACT_PHONE_PATTERN = 'place_order_confirm_contact_phone'


def get_confirm_contact_phone_keyboard() -> InlineKeyboardMarkup:
    return get_confirm_keyboard(
        callback_pattern_start=CONFIRM_CONTACT_PHONE_PATTERN,
    )


CONFIRM_FIO_OR_INN_PATTERN = 'place_order_confirm_fio_or_inn'


def get_confirm_fio_or_inn_keyboard() -> InlineKeyboardMarkup:
    return get_confirm_keyboard(
        callback_pattern_start=CONFIRM_FIO_OR_INN_PATTERN,
    )


CLIENT_TYPE_PATTERN = 'place_order_client_type'


def get_client_type_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(ClientTypeHumanReadable.INDIVIDUAL.value, callback_data=f'{CLIENT_TYPE_PATTERN}_{ClientTypeHumanReadable.INDIVIDUAL.name}'),
                InlineKeyboardButton(ClientTypeHumanReadable.LEGAL.value, callback_data=f'{CLIENT_TYPE_PATTERN}_{ClientTypeHumanReadable.LEGAL.name}'),
            ],
        ]
    )


CONFIRM_ODER_PATTERN = 'place_order_confirm_order'


def get_confirm_order_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton('Изм', callback_data=f'{CONFIRM_ODER_PATTERN}_0'),
            InlineKeyboardButton('Подтвердить', callback_data=f'{CONFIRM_ODER_PATTERN}_1'),
        ],
        [
            InlineKeyboardButton('Отменить', callback_data=f'cancel'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
