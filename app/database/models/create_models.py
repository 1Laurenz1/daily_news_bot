import asyncio

from app.core import logger
from .user import User
from .create_base import engine, Base


async def create_tables(drop_first: bool = False):
    table_names = list(Base.metadata.tables.keys())
    if table_names:
        logger.info(f"Tables to be created: {table_names}")
    else:
        logger.warning("No tables found to create!")

    async with engine.begin() as conn:
        if drop_first:
            logger.info("Dropping all tables before creation...")
            await conn.run_sync(Base.metadata.drop_all)
        logger.info("Creating tables...")
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Tables created successfully!")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_tables(drop_first=True))
    # loop.run_until_complete(create_tables(drop_first=False))