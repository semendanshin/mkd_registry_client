from enum import Enum as pyEnum


class UserRolesEnum(pyEnum):
    """User roles."""

    USER = 'user'
    ADMIN = 'admin'
    SUPER_ADMIN = 'super_admin'


class ClientTypeEnum(pyEnum):
    """Client type enum."""

    INDIVIDUAL = 'individual'
    LEGAL = 'legal'


class OrderStatusEnum(pyEnum):
    """Order status enum."""

    CREATED = 'created'
    INWORK = 'r1r7_in_work'
    R1R7DONE = 'r1r7_done'
    INVOICESENT = 'invoice_sent'
    INVOICEPAID = 'invoice_paid'
    REGISTRYINWORK = 'registry_in_work'
    DONE = 'done'
    CANCLED = 'cancled'

"""
Добавить статус registry_in_work
Переименовать статус in_work в r1r7_in_work
Необходимые статусы
- in_work
- invoice_sent
- done

"""