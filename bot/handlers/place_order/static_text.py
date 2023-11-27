from .enums import PlaceOrderConversationSteps

TEXTS = {
    PlaceOrderConversationSteps.ADDRESS_OR_CADNUMBER: 'Введите адрес вашего дома текстом или кадастровый номер:',
    PlaceOrderConversationSteps.CONTACT_PHONE: 'Укажите номер телефона с WhatsApp для связи с вами:',
    PlaceOrderConversationSteps.CHOOSE_CLIENT_TYPE: 'Счет выставить на физлицо или юрлицо?',
    PlaceOrderConversationSteps.ADD_INN: 'Введите ИНН:',
    PlaceOrderConversationSteps.ADD_FIO: 'Введите ФИО:',
    PlaceOrderConversationSteps.ADD_FIO_FILE: 'Вставьте файл с ФИО собственников в формате Excel (пропустить -> /0):',
}

ADDRESS_AND_CADNUM_CONFIRMATION_TEMPLATE = 'Вы ввели адрес:\n' \
                                           '{address}\n' \
                                           'Кадастровый номер:\n' \
                                           '{cadnum}\n' \
                                           'Все верно?'

CONTACT_PHONE_CONFIRMATION_TEMPLATE = 'Вы ввели номер телефона:\n' \
                                      '{contact_phone}\n' \
                                      'Все верно?'

FIO_CONFIRMATION_TEMPLATE = 'Вы ввели ФИО:\n' \
                            '{fio}\n' \
                            'Все верно?'

INN_CONFIRMATION_TEMPLATE = 'Вы ввели ИНН:\n' \
                            '{inn}\n' \
                            'Название организации:\n' \
                            '{org_name}\n' \
                            'Все верно?'

THANKS_FOR_ORDER = 'Спасибо за вашу заявку!\n' \
                   'Мы уже приступили к выполнению вашего заказа.\n' \
                   'В ближайшее время Вы получите расчет цены за РеестрМКД.'

ORDER_TEMPLATE = '<b>Реестр МКД (с фио без фио?)</b>\n' \
                 '<b>Заказ номер:</b> №\n' \
                 '<b>Кадномер:</b> {cadnum}\n' \
                 '<b>Адрес:</b> {address}\n' \
                 '<b>Ник заказчика:</b> @{username} ({first_name})\n' \
                 '<b>Телефон (WhatsApp):</b> {phone}\n' \
                 '{customer_info}\n' \
                 '{filename}\n'

LEGAL_ORDER_INFO_TEMPLATE = '<b>Юрлицо:</b> {org_name}\n' \
                            '<b>ИНН:</b> {inn}\n'
INDIVIDUAL_ORDER_INFO_TEMPLATE = '<b>Физлицо:</b> {fio}\n'
