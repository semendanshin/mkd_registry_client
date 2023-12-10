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
    INWORK = 'in_work'
    R1R7DONE = 'r1r7_done'
    INVOICESENT = 'invoice_sent'
    INVOICEPAID = 'invoice_paid'
    DONE = 'done'
