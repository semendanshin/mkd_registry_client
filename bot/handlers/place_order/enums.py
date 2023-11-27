from enum import Enum as pyEnum


class PlaceOrderConversationSteps(pyEnum):
    """Conversation steps for the place order dialog."""

    CHOOSE_ACTION = 'choose_action'
    ADDRESS_OR_CADNUMBER = 'address_or_cadnumber'
    CONFIRM_ADDRESS = 'confirm_address'
    CONTACT_PHONE = 'contact_phone'
    CONFIRM_PHONE = 'confirm_phone'
    CHOOSE_CLIENT_TYPE = 'choose_client_type'
    ADD_INN = 'add_inn'
    ADD_FIO = 'add_fio'
    CONFIRM_INN_OR_FIO = 'confirm_inn_or_fio'
    ADD_FIO_FILE = 'add_fio_file'
    CONFIRM_ORDER = 'confirm_order'


class ClientType(pyEnum):
    """Client type enum."""

    INDIVIDUAL = 'individual'
    LEGAL = 'legal'


class ClientTypeHumanReadable(pyEnum):
    """Client type human readable enum."""

    INDIVIDUAL = 'Физ. лицо'
    LEGAL = 'Юр. лицо'
