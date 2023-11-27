from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from config import config

engine = create_async_engine(
    config.db_url.get_secret_value(),
    echo=True,
)
