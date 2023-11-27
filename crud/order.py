from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.models import Order

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
