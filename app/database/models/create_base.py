from sqlalchemy.orm import (
    DeclarativeBase,
    MappedAsDataclass
)
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from app.core import settings


class Base(
    AsyncAttrs,
    DeclarativeBase,
    MappedAsDataclass
):
    pass


engine = create_async_engine(url=settings.DATABASE_URL.get_secret_value())

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=True,
    # echo=True,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False
)