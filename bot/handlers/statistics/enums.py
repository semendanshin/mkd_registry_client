from enum import Enum as pyEnum

from database.enums import OrderStatusEnum


class OrderStatusHumanReadableEnum(pyEnum):
    """Order status enum."""

    CREATED = 'Создан'
    INWORK = 'Р1Р7 в работе'
    R1R7DONE = 'Р1Р7 готов'
    INVOICESENT = 'Счет отправлен'
    INVOICEPAID = 'Счет оплачен'
    REGISTRYINWORK = 'Реестр в работе'
    DONE = 'Готов'
    CANCLED = 'Отменен'

    @classmethod
    def get_human_readable(cls, status: OrderStatusEnum) -> str:
        return cls[status.name].value
