from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.models import Order
from database.enums import OrderStatusEnum

from schemas.order import OrderCreate


async def create_order(session: AsyncSession, order: OrderCreate) -> Order:
    order = Order(**order.model_dump())
    session.add(order)
    await session.commit()
    await session.refresh(order)

    return order


async def get_order(session: AsyncSession, order_id: int) -> Order:
    result = await session.execute(select(Order).filter(Order.id == order_id))
    return result.scalars().first()


async def get_order_by_egrn_request_id(session: AsyncSession, egrn_request_id: int) -> Order:
    result = await session.execute(select(Order).filter(Order.egrn_request_id == egrn_request_id))
    return result.scalars().first()


async def update_order(session: AsyncSession, order_id: int, **kwargs) -> Order:
    order = await get_order(session, order_id)
    for key, value in kwargs.items():
        if hasattr(order, key):
            setattr(order, key, value)
    await session.commit()
    await session.refresh(order)
    return order


async def get_orders(session: AsyncSession) -> list[Order]:
    result = await session.execute(select(Order))
    return list(result.scalars().all())


async def get_orders_by_status(session: AsyncSession, status: OrderStatusEnum) -> list[Order]:
    result = await session.execute(select(Order).filter(Order.status == status))
    return list(result.scalars().all())


async def get_orders_by_user_id(session: AsyncSession, user_id: int) -> list[Order]:
    result = await session.execute(select(Order).filter(Order.user_id == user_id))
    return list(result.scalars().all())


async def get_orders_by_statuses(session: AsyncSession, statuses: list[OrderStatusEnum]) -> list[Order]:
    result = await session.execute(select(Order).filter(Order.status.in_(statuses)))
    return list(result.scalars().all())
