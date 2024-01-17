from sqlalchemy import select, update, func, and_, or_, not_
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User
from schemas.user import UserCreate
from database.enums import UserRolesEnum, OrderStatusEnum
from typing import Optional


async def get_user(session: AsyncSession, user_id: int) -> Optional[User]:
    result = await session.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> Optional[User]:
    result = await session.execute(select(User).filter(User.username == username))
    user = result.scalars().first()
    return user


async def create_user(session: AsyncSession, user: UserCreate) -> User:
    if await get_user(session, user.id):
        raise ValueError('This user already exists')

    user = User(**user.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def update_user(session: AsyncSession, new_data: UserCreate) -> User:
    user = await get_user(session, new_data.id)
    if not user:
        raise ValueError('This user does not exist')

    for key, value in new_data.model_dump().items():
        if value is not None and key != 'id' and key != 'role':
            setattr(user, key, value)

    await session.commit()
    await session.refresh(user)
    return user


async def update_user_role(session: AsyncSession, username: str, role: UserRolesEnum) -> User:
    await session.execute(update(User).where(User.username == username).values(role=role))
    await session.commit()
    return await get_user_by_username(session, username)


async def get_admins(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User).filter(User.role == UserRolesEnum.ADMIN))
    return list(result.scalars().all())


async def get_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User))
    return list(result.scalars().all())


async def get_non_clients(session: AsyncSession) -> list[User]:
    # non-client is user who have 0 placed orders with status != 'canceled' or 'created'
    statement = select(User).join(User.orders).where(
        func.count(
            User.orders
        ) -
        func.count(
            User.orders.filter(
                or_(
                    User.orders.any(status=OrderStatusEnum.CANCLED),
                    User.orders.any(status=OrderStatusEnum.CREATED),
                )
            )
        ) == 0,
    )
    result = await session.execute(statement)
    return list(result.scalars().all())


async def get_clients(session: AsyncSession) -> list[User]:
    # client is user who have >0 placed orders with status != 'canceled' or 'created'
    statement = select(User).join(User.orders).where(
        func.count(
            User.orders
        ) -
        func.count(
            User.orders.filter(
                or_(
                    User.orders.any(status=OrderStatusEnum.CANCLED),
                    User.orders.any(status=OrderStatusEnum.CREATED),
                )
            )
        ) > 0,
    )
    result = await session.execute(statement)
    return list(result.scalars().all())


async def is_client(session: AsyncSession, user_id: int) -> bool:
    statement = select(User).join(User.orders).where(
        and_(
            User.id == user_id,
            not_(or_(User.orders.any(status=OrderStatusEnum.CREATED), User.orders.any(status=OrderStatusEnum.CREATED))),
            func.count(User.orders) > 0
        )
    )
    result = await session.execute(statement)
    return bool(result.scalars().first())
